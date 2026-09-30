# Getting started is four commands, and `make setup` is all of them.
#
# UV_PROJECT_ENVIRONMENT is set on every uv call on purpose: this project's environment is
# `.venv-corpus`, not the conventional `.venv`, so that it cannot collide with the corpus
# translation tooling that already lives in this repo. Without the variable `uv` silently
# builds the wrong environment and every later command fails somewhere else.

VENV := .venv-corpus
PY   := $(VENV)/bin/python
UV   := UV_PROJECT_ENVIRONMENT=$(VENV) uv
OWNER_DSN ?= postgresql+psycopg://corpus_owner:corpus_local_dev@127.0.0.1:5433/sanskrit_texts
TEST_DSN  ?= postgresql+psycopg://corpus_owner:corpus_local_dev@127.0.0.1:5433/sanskrit_texts_test

# NOT Docker, since 2026-09-29. Docker defined exactly one service here -- a postgres:16 --
# and the Docker Desktop VM disk failed, taking the store with it. This is a SECOND Homebrew
# cluster (postgresql@18) with its own data directory; the default brew instance runs on 5435
# for obsidian-vk-publish and must not be shared. 5433 is fixed by ports.yml AND by
# sanskrit_texts/dsn_guard.py EXPECTED_PORT -- change one without the other and the guard lies.
PGDATA_CORPUS := /opt/homebrew/var/sanskrit-texts-pg
PG_PLIST      := $(HOME)/Library/LaunchAgents/com.rupali.sanskrit-texts-postgres.plist

.PHONY: help setup deps db migrate testdb import hello export test check clean-db backup

help:  ## show this
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'

setup: deps db migrate testdb  ## everything: deps, local cluster, schema, test database
	@echo
	@echo "Ready. Try:  make hello"

deps:  ## create .venv-corpus and install
	$(UV) sync --extra dev

db:  ## start the local postgres on 5433 and wait for a REAL catalog read
	@launchctl list 2>/dev/null | grep -q com.rupali.sanskrit-texts-postgres \
	  || launchctl load $(PG_PLIST)
	@# pg_isready is NOT the readiness check, and this is not a style preference. On 2026-09-29 it
	@# reported "accepting connections" for 13 days against a cluster that could not read
	@# global/pg_filenode.map. It proves a postmaster is listening; only a catalog read proves the
	@# cluster can be used. rule:discernment-checks 1 -- a check that cannot fail is worse than none.
	@until psql -h 127.0.0.1 -p 5433 -U corpus_owner -d postgres -tAc 'select 1' >/dev/null 2>&1; \
	  do sleep 1; done
	@echo "postgres ready on 5433 (catalog read OK, not merely listening)"

migrate:  ## create the schema, the published views and the read-only API role
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(VENV)/bin/alembic upgrade head

testdb:  ## the suite's own database — the TRUNCATE guard requires the _test suffix (G59)
	@psql -h 127.0.0.1 -p 5433 -U corpus_owner -d postgres -tAc \
	  "SELECT 1 FROM pg_database WHERE datname='sanskrit_texts_test'" | grep -q 1 || \
	  createdb -h 127.0.0.1 -p 5433 -U corpus_owner -O corpus_owner sanskrit_texts_test
	CORPUS_OWNER_DSN="$(TEST_DSN)" $(VENV)/bin/alembic upgrade head

hello:  ## the fast loop: one small text, nothing written
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(PY) -m sanskrit_texts.importer --dry-run --text yajusha_jyotisham

import:  ## the whole corpus, accepting the 70 known duplicate labels (G8). Exits 1 while they exist.
	# Without --allow-partial this target could never commit: the 70 are real data defects the
	# importer names and refuses, by design. The flag accepts THEM; a new violation still prints.
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(PY) -m sanskrit_texts.importer --all --allow-partial

export:  ## fidelity export — the cutover gate's input
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(PY) -m sanskrit_texts.export --mode fidelity --all --out /tmp/rt

test:  ## the suite, with a missing database treated as a FAILURE rather than a skip
	CORPUS_REQUIRE_DB=1 $(VENV)/bin/pytest tests/ -q

backup:  ## dump the store AND restore it into a scratch db to prove the dump works (T5.4)
	@# DECISIONS.md requires ONE TESTED restore before the DB is authoritative, and on 2026-09-29
	@# the store died with no dump at all. `verify` is why the dump can be believed: a backup that
	@# has never been restored is found broken at the moment it is needed.
	./scripts/backup_store.sh all

check:  ## registry vs corpus reconciliation
	python3 scripts/check_inventory.py

clean-db:  ## drop every table and start over — refuses non-local, asks before dropping
	@$(PY) -m sanskrit_texts.dsn_guard --dsn "$(OWNER_DSN)"
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(VENV)/bin/alembic downgrade base
