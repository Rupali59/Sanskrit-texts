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

.PHONY: help setup deps db migrate testdb import hello export test check clean-db

help:  ## show this
	@grep -E '^[a-z-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*?## "}{printf "  %-10s %s\n",$$1,$$2}'

setup: deps db migrate testdb  ## everything: deps, container, schema, test database
	@echo
	@echo "Ready. Try:  make hello"

deps:  ## create .venv-corpus and install
	$(UV) sync --extra dev

db:  ## start postgres on 5433 and wait for it
	docker compose up -d
	@until docker compose exec -T postgres pg_isready -U corpus_owner -q 2>/dev/null; do sleep 1; done
	@echo "postgres ready on 5433"

migrate:  ## create the schema, the published views and the read-only API role
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(VENV)/bin/alembic upgrade head

testdb:  ## the suite's own database — the TRUNCATE guard requires the _test suffix (G59)
	@docker compose exec -T postgres psql -U corpus_owner -d postgres -tc \
	  "SELECT 1 FROM pg_database WHERE datname='sanskrit_texts_test'" | grep -q 1 || \
	  docker compose exec -T postgres createdb -U corpus_owner sanskrit_texts_test
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

check:  ## registry vs corpus reconciliation
	python3 scripts/check_inventory.py

clean-db:  ## drop every table and start over (local only)
	CORPUS_OWNER_DSN="$(OWNER_DSN)" $(VENV)/bin/alembic downgrade base
