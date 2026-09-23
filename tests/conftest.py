"""Fixtures for the corpus store tests.

TWO ROLES, NEVER ONE. `owner_engine` is the migration/ingest identity; `api_engine` is what a
consumer gets. They must be different Postgres roles, because a table OWNER can re-grant past
any REVOKE and is not subject to RLS unless it is FORCEd — so a publication gate built on
GRANT is worth nothing if the application connects as owner. docker-compose.yml creates only
the owner; the API role is created by the migration.
"""

from __future__ import annotations

import os
import urllib.parse

import pytest
import sqlalchemy as sa
from sqlalchemy.engine import Engine

from sanskrit_texts.dsn_guard import assert_local_store

# docker-compose.yml maps the container's 5432 to host 5433 — NOT 5432, which
# ports.yml allocates to Divyansh/AuroraV3/postgres-forward.
OWNER_DSN = os.environ.get(
    "CORPUS_OWNER_DSN",
    "postgresql+psycopg://corpus_owner:corpus_local_dev@127.0.0.1:5433/sanskrit_texts_test",
)
API_DSN = os.environ.get(
    "CORPUS_API_DSN",
    "postgresql+psycopg://corpus_api:corpus_api_local@127.0.0.1:5433/sanskrit_texts_test",
)


# T4/G61, 2026-09-16. A skip is an attributable absence, which is right -- but nothing
# converted it into a FAILURE, and CI has no Postgres. So the publication gate could report
# green having asserted nothing at all: `pytest -q` prints `s`, not `F`, and nobody reads the
# `s`. Set CORPUS_REQUIRE_DB=1 (CI does) and a missing database becomes a hard failure.
# rule:enforcement-watches-itself -- "found nothing" and "looked at nothing" must differ.
REQUIRE_DB = os.environ.get("CORPUS_REQUIRE_DB", "").strip() not in ("", "0", "false", "no")


def _engine_or_skip(dsn: str, who: str) -> Engine:
    """Connect, or skip with the reason -- or FAIL, when the DB is declared required.

    A test that silently passes because the database is absent is worse than no test
    (rule:discernment-checks §1). SKIP is an attributable absence; a green tick is not.
    """
    engine = sa.create_engine(dsn, future=True)
    try:
        with engine.connect() as conn:
            conn.execute(sa.text("select 1"))
    except Exception as exc:  # noqa: BLE001 - the reason is the point
        where = dsn.split("@")[-1]
        detail = f"no {who} connection ({where}): {type(exc).__name__}: {exc}"
        if REQUIRE_DB:
            pytest.fail(
                f"CORPUS_REQUIRE_DB is set and the gate cannot be enforced -- {detail}. "
                "This is a FAILURE, not a skip: an unenforced gate must never read as a pass."
            )
        pytest.skip(detail)
    return engine


@pytest.fixture(scope="session")
def owner_engine() -> Engine:
    return _engine_or_skip(OWNER_DSN, "owner")


@pytest.fixture(scope="session")
def api_engine() -> Engine:
    """The consumer identity. Created by the migration, so this skips until it has run."""
    return _engine_or_skip(API_DSN, "api-role")


LOCAL_HOSTS = frozenset({"127.0.0.1", "localhost", "::1", ""})
EXPECTED_PORT = 5433  # ports.yml allocates this to Vipin Kaushik/sanskrit-texts/postgres
# Host+port alone was not enough, and the gap showed up the moment the corpus was real: the
# development database `sanskrit_texts` is ALSO on localhost:5433, so a test run would have
# truncated the 97,724 verses that had just been imported into it. The suite gets its own
# database and the guard requires the suffix.
TEST_DB_SUFFIX = "_test"


def assert_truncatable(dsn: str) -> None:
    """Refuse to TRUNCATE anything that is not the local development store.

    T2/G59, 2026-09-16. This fixture used to truncate whatever CORPUS_OWNER_DSN named, with
    no check at all -- so exporting that variable at a real store and running `pytest`
    destroyed the corpus, with no error, because truncating is exactly what the fixture is
    for. rule:safety-flag-needs-a-test: the unsafe path must be proven UNREACHABLE, not
    merely guarded, which is what tests/test_schema_guards.py does (this docstring named a
    `tests/test_truncate_guard.py` that has never existed -- corrected 2026-09-23).

    The host/port half is `sanskrit_texts.dsn_guard.assert_local_store`, shared with
    `make clean-db`'s preflight so the two cannot drift. The `_test` clause below is this
    caller's own, and is the half that actually bites: the dev corpus is on the same host
    and port.

    Escape hatch is explicit and loud: CORPUS_ALLOW_TRUNCATE=1.
    """
    if os.environ.get("CORPUS_ALLOW_TRUNCATE", "").strip() in ("1", "true", "yes"):
        return
    database = (urllib.parse.urlsplit(dsn).path or "").lstrip("/")
    try:
        assert_local_store(dsn, "TRUNCATE")
    except RuntimeError as e:
        raise RuntimeError(
            f"{e} Set CORPUS_ALLOW_TRUNCATE=1 if you genuinely mean to empty this database."
        ) from None
    if not database.endswith(TEST_DB_SUFFIX):
        raise RuntimeError(
            f"refusing to TRUNCATE database {database!r}: the suite only empties a database "
            f"whose name ends {TEST_DB_SUFFIX!r}. The development corpus lives on this same "
            f"host and port, and truncating it would destroy a real import. "
            f"Create it with: CREATE DATABASE {database}{TEST_DB_SUFFIX} OWNER corpus_owner"
        )


@pytest.fixture()
def clean_corpus(owner_engine: Engine):
    """Empty the corpus tables around each test, without dropping them.

    TRUNCATE ... CASCADE rather than DROP: the tests assert against the real migrated schema,
    including its views and grants. A test that builds its own tables proves nothing about the
    schema that ships.
    """
    assert_truncatable(str(owner_engine.url))
    tables = "text, section, verse, annotation, annotation_revision"
    with owner_engine.begin() as conn:
        conn.execute(sa.text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
    yield
    with owner_engine.begin() as conn:
        conn.execute(sa.text(f"TRUNCATE {tables} RESTART IDENTITY CASCADE"))
