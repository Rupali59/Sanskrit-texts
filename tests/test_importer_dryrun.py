"""T1: `--dry-run` must write nothing -- and "nothing" means every table, not just an empty count.

THE RULE THIS CLOSES. `rule:safety-flag-needs-a-test` records three paid instances of a safety
flag that was read but never tested: `digest.mjs --dry-run` ran an armed deletion while its own
header promised "print, write NO state", because `dryRun` was checked in one function and not
in the lifecycle sweep it called. `sanskrit_texts.importer --dry-run` makes the identical
promise -- "DRY RUN (nothing written)" -- to zero tests, in a repo whose whole reason to exist
is that the database becomes authoritative for editing. This is the test that closes it, per T1
of the 2026-09-16 task list.

WHAT "UNCHANGED" MEANS HERE. Not `count(*)`: a dry run that deleted one row and inserted a
different one would pass a count check and still be a real loss (`rule:safety-flag-needs-a-test`
names this exact shape). `_snapshot` hashes the CONTENT of every table -- Postgres's own
composite-row text representation, sorted so physical/insertion order cannot matter -- next to
the count, so a row added, removed, or substituted moves the digest even when the count does
not.

THE CASE A NAIVE TEST MISSES. An empty database looks "unchanged" no matter what a dry run does
to it -- that is absence of evidence, not evidence of absence.
`test_dry_run_leaves_a_populated_database_untouched` imports one real text first, so the
assertion is made over data that could actually be lost.

TWO CODE PATHS, COVERED SEPARATELY. `laghu_jatakam` (14 duplicate `(chapter, shloka)` labels)
and `minaraja_yavana_jataka` (1) both trip `uq_verse_label_in_section` on the bulk insert and
are re-run through the importer's SLOW per-verse path (`enumerate_all=True` -- see
`importer.py`'s "SLOW PATH" comment) so every offending label is named instead of just the
first. That is a materially different set of INSERT statements from the fast bulk path used by
a clean text, and a flag can guard one path while leaving its sibling reachable -- so both are
asserted here rather than inferred from the fast path passing.

THE MUTATION, AND A FINDING IT SURFACED (2026-09-16, this session). Neutralising `if dry_run:`
in `importer.run` -- the exact line that decides `outer.rollback()` vs falling through to
`outer.commit()` -- does NOT turn every test in this file red. `--all`, `laghu_jatakam` and
`minaraja_yavana_jataka` all carry pre-existing constraint violations (the 70 G8 duplicates
across the corpus), and `run()` already rolls back on ANY unresolved violation via the sibling
`elif result.violations and not allow_partial:` branch -- *regardless* of `dry_run`. So those
three cases stay green under the mutation for a real, unrelated reason, not because the
dry-run guard is intact. Only the violation-free cases -- a single clean text, and the second
text in the non-empty-database test -- isolate `dry_run` as the SOLE thing standing between the
run and a commit, and only those two actually went red. Recorded here rather than smoothed
over, per `rule:discernment-checks`: a suite that reports exactly what it proved is worth more
than one that claims uniform failure it did not check for.
"""

from __future__ import annotations

import sqlalchemy as sa

from sanskrit_texts import importer
from tests.conftest import OWNER_DSN

# Every table the importer writes. `t::text` is Postgres's own composite-row representation, so
# this needs no per-table column list and covers `text_facet`'s composite key the same way it
# covers `verse`'s serial one. Sorting the row strings before hashing makes the digest
# independent of insertion / physical order, which a bare positional comparison would not be.
TABLES = ("category", "text", "text_facet", "section", "verse", "annotation",
          "annotation_revision")


def _snapshot(conn: sa.Connection) -> dict[str, tuple[int, str]]:
    """count(*) AND a content hash, per table.

    count(*) alone passes a dry run that deleted one row and inserted a different one -- exactly
    the shape `rule:safety-flag-needs-a-test` names as the check that "trusts the tool's own
    description of itself". The hash is over row CONTENT, not row identity, so a
    delete-then-reinsert-of-an-identical-row is (correctly) invisible; only an actual change in
    what a table holds moves the digest.
    """
    out: dict[str, tuple[int, str]] = {}
    for table in TABLES:
        count, digest = conn.execute(
            sa.text(
                f"SELECT count(*), coalesce(md5(string_agg(t::text, '|' ORDER BY t::text)), '')"
                f" FROM {table} t"
            )
        ).one()
        out[table] = (count, digest)
    return out


def _assert_unchanged(engine: sa.Engine, before: dict[str, tuple[int, str]]) -> None:
    with engine.connect() as conn:
        after = _snapshot(conn)
    assert after == before, (
        "dry-run changed the database -- the unsafe path was reachable. "
        f"before={before} after={after}"
    )


# --------------------------------------------------------------------------------------
# `--dry-run --all`
# --------------------------------------------------------------------------------------
def test_dry_run_all_writes_nothing(owner_engine, clean_corpus):
    with owner_engine.connect() as conn:
        before = _snapshot(conn)
    # allow_partial=True is what makes this test MEAN something. Without it the
    # sibling `elif result.violations and not allow_partial` branch rolls back too,
    # so neutralising `dry_run` leaves the test green and it proves nothing about the
    # flag. With it, `dry_run` is the ONLY thing standing between this import and a
    # commit -- which is the property the rule asks to be shown unreachable.
    result = importer.run(OWNER_DSN, only=None, dry_run=True, allow_partial=True)
    assert result.texts > 0, "the dry run must have actually walked the corpus, not no-opped"
    _assert_unchanged(owner_engine, before)


# --------------------------------------------------------------------------------------
# `--dry-run --text <one slug>` -- the fast bulk-insert path, a text with no duplicates
# --------------------------------------------------------------------------------------
def test_dry_run_single_clean_text_writes_nothing(owner_engine, clean_corpus):
    with owner_engine.connect() as conn:
        before = _snapshot(conn)
    result = importer.run(OWNER_DSN, only={"yajusha_jyotisham"}, dry_run=True)
    assert result.texts == 1
    assert not result.violations, "yajusha_jyotisham is not one of the G8 duplicate texts"
    _assert_unchanged(owner_engine, before)


# --------------------------------------------------------------------------------------
# `--dry-run --text <known duplicate>` -- the SLOW per-verse path (importer.py: "SLOW PATH")
# --------------------------------------------------------------------------------------
def test_dry_run_laghu_jatakam_writes_nothing(owner_engine, clean_corpus):
    """14 duplicate (chapter, shloka) labels -- verified against a live dry run 2026-09-16,
    matches DECISIONS.md / the plan brief. Re-derive with `python3 scripts/check_inventory.py`
    before trusting this number if the corpus changes."""
    with owner_engine.connect() as conn:
        before = _snapshot(conn)
    result = importer.run(OWNER_DSN, only={"laghu_jatakam"}, dry_run=True,
                          allow_partial=True)   # isolate dry_run; see the --all test
    assert len(result.violations) == 14, (
        f"expected 14 known duplicates in laghu_jatakam, got {len(result.violations)}"
    )
    _assert_unchanged(owner_engine, before)


def test_dry_run_minaraja_yavana_jataka_writes_nothing(owner_engine, clean_corpus):
    """1 duplicate label -- verified against a live dry run 2026-09-16."""
    with owner_engine.connect() as conn:
        before = _snapshot(conn)
    result = importer.run(OWNER_DSN, only={"minaraja_yavana_jataka"}, dry_run=True,
                          allow_partial=True)   # isolate dry_run; see the --all test
    assert len(result.violations) == 1, (
        f"expected 1 known duplicate in minaraja_yavana_jataka, got {len(result.violations)}"
    )
    _assert_unchanged(owner_engine, before)


# --------------------------------------------------------------------------------------
# Non-empty database -- the case a naive test misses, because an empty one looks unchanged
# no matter what a dry run does to it.
# --------------------------------------------------------------------------------------
def test_dry_run_leaves_a_populated_database_untouched(owner_engine, clean_corpus):
    """Import one real text for real, THEN dry-run a second, unrelated text, and prove the
    first survives byte-for-byte. Both are violation-free and tiny on purpose -- this test is
    about the dry run's honesty, not about import performance."""
    seed = importer.run(OWNER_DSN, only={"sarvasara_upanishad"}, dry_run=False)
    assert seed.texts == 1 and not seed.violations, "the seed import itself must have landed"

    with owner_engine.connect() as conn:
        before = _snapshot(conn)
    assert before["text"][0] == 1, "the seeded text must be visible before the dry run runs"

    result = importer.run(OWNER_DSN, only={"jabala_upanishad"}, dry_run=True)
    assert result.texts == 1 and not result.violations
    _assert_unchanged(owner_engine, before)
