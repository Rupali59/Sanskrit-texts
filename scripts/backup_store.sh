#!/usr/bin/env bash
# Back up the corpus store, and PROVE the backup restores.
#
# WHY THIS EXISTS, AND WHY IT SHIPS WITH ITS OWN RESTORE. `DECISIONS.md:813-814` requires "ONE
# tested restore -- drop the volume, restore, round trip -- before the DB is authoritative", and
# `STATE.md` carried that as open from 2026-09-17. On 2026-09-29 the store became unreadable when
# the Docker Desktop VM disk failed, and there was no dump. Nothing irreplaceable was lost, but
# only because of WHEN it happened: the corpus JSON is the source of truth and zero annotations
# had been approved. The moment one is, that luck expires.
#
# `rule:name-what-no-test-executes`: a backup that has never been restored is discovered broken at
# exactly the moment it is needed. So `verify` is not optional documentation -- it is the reason
# the `backup` half can be believed, and it runs the real restore against a real cluster.
#
# TWO DUMPS, NOT ONE, AND THE SECOND IS THE ONE PEOPLE FORGET. `pg_dump` of a database does NOT
# carry roles. `corpus_api` -- the read-only role that IS the publication gate -- lives in the
# cluster, not the database, so a database-only dump restores a corpus whose gate has no grantee.
# `--globals-only` captures it.
#
#   ./scripts/backup_store.sh backup    # dump database + globals, prune to the last 7
#   ./scripts/backup_store.sh verify    # restore the newest dump into a scratch db and compare
#   ./scripts/backup_store.sh           # both -- this is what `make backup` runs
#
# Exit: 0 ok, 1 a check failed, 2 refused (wrong host/port, or nothing to verify).

set -euo pipefail

PGHOST=127.0.0.1
PGPORT=5433          # ports.yml AND sanskrit_texts/dsn_guard.py EXPECTED_PORT. Change neither alone.
PGUSER=corpus_owner
DB=sanskrit_texts
SCRATCH=sanskrit_texts_restorecheck
KEEP=7
BACKUP_DIR="${CORPUS_BACKUP_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)/sanskrit-texts-backups}"
export PGHOST PGPORT PGUSER

# The scratch database is DROPPED by `verify`. Refuse to run anywhere but the local corpus store,
# and refuse outright if the scratch name is ever the real one -- the same shape as
# `sanskrit_texts/dsn_guard.py`, whose lesson (G59) was that host+port felt sufficient and was not:
# the development corpus lives on this same host and port.
guard() {
  [[ "$SCRATCH" != "$DB" ]] || { echo "refusing: scratch name equals the real database" >&2; exit 2; }
  [[ "$PGHOST" == "127.0.0.1" || "$PGHOST" == "localhost" ]] || {
    echo "refusing: host $PGHOST is not the local corpus store" >&2; exit 2; }
  [[ "$PGPORT" == "5433" ]] || { echo "refusing: port $PGPORT is not 5433" >&2; exit 2; }
}

# A real catalog read. NOT pg_isready -- it reported "accepting connections" for the entire 13
# days the cluster could not read global/pg_filenode.map, which is how the 2026-09-29 failure went
# unnoticed. `rule:discernment-checks` 1.
alive() { psql -d postgres -tAc 'select 1' >/dev/null 2>&1; }

counts() {  # row counts + the gate, as one comparable blob
  psql -d "$1" -tAF'|' -c "
    select 'text',count(*) from text
    union all select 'section',count(*) from section
    union all select 'verse',count(*) from verse
    union all select 'annotation',count(*) from annotation
    union all select 'revision',count(*) from annotation_revision
    union all select 'published_verse',count(*) from published_verse
    union all select 'published_value_not_null',count(value) from published_verse
    union all select 'api_grants',count(*) from information_schema.role_table_grants
             where grantee='corpus_api'
    order by 1"
}

do_backup() {
  mkdir -p "$BACKUP_DIR"
  local stamp; stamp=$(date +%Y%m%d-%H%M%S)
  local dump="$BACKUP_DIR/$DB-$stamp.dump"
  local globals="$BACKUP_DIR/globals-$stamp.sql"

  pg_dump -d "$DB" -Fc -f "$dump"
  pg_dumpall --globals-only -f "$globals"

  # A dump that pg_restore cannot list is not a backup. Check before pruning anything.
  pg_restore -l "$dump" >/dev/null || { echo "FAIL: pg_restore cannot read $dump" >&2; exit 1; }

  printf '  dump    %s  (%s)\n' "$(basename "$dump")" "$(du -h "$dump" | cut -f1)"
  printf '  globals %s  (%s)\n' "$(basename "$globals")" "$(du -h "$globals" | cut -f1)"

  # Prune oldest first, keeping KEEP of each. Never touches anything but our own name pattern.
  ls -1t "$BACKUP_DIR/$DB-"*.dump 2>/dev/null | tail -n +$((KEEP + 1)) | while read -r f; do
    rm -f -- "$f"; echo "  pruned  $(basename "$f")"
  done
  ls -1t "$BACKUP_DIR/globals-"*.sql 2>/dev/null | tail -n +$((KEEP + 1)) | while read -r f; do
    rm -f -- "$f"; echo "  pruned  $(basename "$f")"
  done
}

do_verify() {
  local dump; dump=$(ls -1t "$BACKUP_DIR/$DB-"*.dump 2>/dev/null | head -1) || true
  [[ -n "${dump:-}" ]] || { echo "refusing: no dump in $BACKUP_DIR to verify" >&2; exit 2; }
  echo "  restoring $(basename "$dump") into $SCRATCH"

  dropdb --if-exists "$SCRATCH"
  createdb -O "$PGUSER" "$SCRATCH"
  # --exit-on-error: a restore that reports success having skipped half its objects is the
  # failure this whole script exists to prevent.
  pg_restore -d "$SCRATCH" --no-owner --exit-on-error "$dump"

  local before after
  before=$(counts "$DB")
  after=$(counts "$SCRATCH")

  echo "  --- live vs restored ---"
  paste -d'\n' <(echo "$before") <(echo "$after") >/dev/null 2>&1 || true
  echo "$before" | while IFS='|' read -r k v; do
    local v2; v2=$(echo "$after" | awk -F'|' -v k="$k" '$1==k{print $2}')
    printf '  %-26s live=%-10s restored=%-10s %s\n' "$k" "$v" "$v2" \
      "$([[ "$v" == "$v2" ]] && echo OK || echo MISMATCH)"
  done

  local rc=0
  if [[ "$before" != "$after" ]]; then
    echo "FAIL: restored database does not match the live one" >&2; rc=1
  fi

  # The gate must survive the restore, not merely the rows. A restored corpus that serves drafts
  # is a worse outcome than no backup.
  local leaked
  leaked=$(psql -d "$SCRATCH" -tAc "select count(value) from published_verse")
  if [[ "$leaked" != "0" ]]; then
    echo "FAIL: published_verse in the restored db exposes $leaked values while nothing is approved" >&2
    rc=1
  else
    echo "  gate holds in the restored db: published_verse exposes 0 values"
  fi

  dropdb --if-exists "$SCRATCH"
  echo "  scratch dropped"
  return $rc
}

guard
alive || { echo "refusing: no catalog read from $PGHOST:$PGPORT -- the cluster is not usable" >&2; exit 2; }

case "${1:-all}" in
  backup) do_backup ;;
  verify) do_verify ;;
  all)    do_backup; do_verify ;;
  *)      echo "usage: $0 [backup|verify|all]" >&2; exit 2 ;;
esac
