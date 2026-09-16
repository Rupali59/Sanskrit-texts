"""The publication gate — the test G50 has needed since the gate was invented by accident.

WHAT THIS DEFENDS. The workspace hard rule is "computation is AI-assisted; meaning is not":
no machine-written interpretation reaches a public surface. In the MongoDB path that rule is
enforced by `astroacharya/scripts/seed_texts.py`'s `_normalize_shloka`, a 12-key allowlist,
and by nothing else — `app/api/texts.py` returns the document wholesale. The allowlist is an
ingest function that became an editorial policy by accident, and G50 records that its own
description of itself was wrong by eight keys.

HOW THIS IS DIFFERENT. Here the gate is a database privilege, not a Python dict comprehension:
the published surface is a VIEW over `state='approved'` rows, and the API role holds SELECT on
the views and nothing at all on `annotation` / `annotation_revision`.

THREE TESTS, AND THE THIRD IS WHY THE FIRST MEANS ANYTHING.

  1. a draft's bytes appear in NO published surface
  2. the API role cannot read the underlying tables even deliberately
  3. **the same bytes DO appear once published** — the negative control

Without (3), test (1) passes just as happily against an empty view, a broken join, or a
misspelled table name. `rule:discernment-checks` §1: every check ships with the input that
makes it fail. (3) is that input.

SNAPSHOT BYTES, DO NOT GREP FOR "draft". A guard that trusts the system's own description of
itself is the failure it exists to catch.
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa
from sqlalchemy.engine import Engine

# Postgres' SQLSTATE for insufficient_privilege. M5/2026-09-16: this file used to assert the
# STRING "permission denied", which is locale- and version-dependent -- and worse, a different
# ProgrammingError (a renamed table, say) was caught by the same `except` and reported as a
# message mismatch rather than as "the table is gone".
INSUFFICIENT_PRIVILEGE = "42501"

# Chosen to be impossible in real corpus text or in any translation: no Devanagari, no English
# word, and a hex tail. If this string turns up in a published byte stream it got there from
# the draft row and from nowhere else.
SENTINEL = "ZZ-UNPUBLISHED-DRAFT-MUST-NOT-LEAK-7f3a91-ZZ"

def published_views(conn: sa.Connection) -> tuple[str, ...]:
    """DERIVE the published surface; never hardcode it.

    G17/T11: this was a hardcoded 2-tuple, so a view added to the migration tomorrow would be
    untested by construction and the gate would report green having never looked at it. A
    check that cannot see a new surface is a check that cannot fail on one.
    """
    rows = conn.execute(
        sa.text(
            "SELECT table_name FROM information_schema.views "
            "WHERE table_schema = 'public' ORDER BY table_name"
        )
    ).scalars().all()
    assert rows, "no published views found -- the migration has not run, or they were renamed"
    return tuple(rows)


def _seed(conn: sa.Connection, *, state: str) -> None:
    """One text -> one section -> one verse -> one annotation carrying the sentinel."""
    conn.execute(
        sa.text(
            "INSERT INTO text (id, title_sa, title_en, category, structure)"
            " VALUES ('gate_probe', 'परीक्षा', 'Gate Probe', 'parashari', '{}'::jsonb)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO section (id, text_id, parent_id, depth, level_name, label, position)"
            " VALUES (1, 'gate_probe', NULL, 1, 'chapter', '1', 1)"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO verse (id, section_id, number_label, position, devanagari)"
            " VALUES (1, 1, '1', 1, 'अथातो धर्मजिज्ञासा')"
        )
    )
    conn.execute(
        sa.text(
            "INSERT INTO annotation (id, verse_id, kind, lang, value, state)"
            " VALUES (1, 1, 'translation', 'en', :v, :s)"
        ),
        {"v": SENTINEL, "s": state},
    )


def _published_bytes(conn: sa.Connection) -> str:
    """Every byte every published surface can emit, concatenated.

    Deliberately reads `SELECT *` and stringifies whole rows rather than naming the columns a
    draft would live in. Naming them would assume the leak's shape; this assumes only that a
    leak is bytes.
    """
    out: list[str] = []
    for view in published_views(conn):
        for row in conn.execute(sa.text(f"SELECT * FROM {view}")).mappings():
            out.append("|".join(f"{k}={v!r}" for k, v in row.items()))
    return "\n".join(out)


@pytest.mark.parametrize("read_as", ["owner", "api"])
def test_a_draft_never_appears_in_any_published_surface(
    owner_engine: Engine, api_engine: Engine, clean_corpus, read_as: str
):
    """T11/M4, 2026-09-16: read the views as the CONSUMER, not only as the owner.

    Both content tests used to run entirely on `owner_engine`, so the assertion that actually
    matters -- what a consumer can see contains no draft bytes -- was never made from the
    consumer's identity. The owner can see everything by construction, so passing as owner
    says nothing about what `corpus_api` gets.
    """
    with owner_engine.begin() as conn:
        _seed(conn, state="draft")
    reader = owner_engine if read_as == "owner" else api_engine
    with reader.connect() as conn:
        blob = _published_bytes(conn)
    assert SENTINEL not in blob, (
        f"a draft annotation's bytes reached a published view, read as {read_as} — this is "
        f"the G50 leak, in the new schema"
    )


def test_the_same_bytes_DO_appear_once_published(
    owner_engine: Engine, api_engine: Engine, clean_corpus
):
    """The negative control. If this fails, the test above is vacuous, not passing.

    A published surface that cannot carry the sentinel EVEN WHEN the row is published is an
    empty view or a broken join, and the absence test above would be green for the wrong
    reason.
    """
    with owner_engine.begin() as conn:
        # T6, 2026-09-16: the servable state is `approved`, not `published`. This line said
        # "published" and the CHECK constraint rejected it the first time the suite ran after
        # the five-state change -- which is the constraint working, not a regression.
        _seed(conn, state="approved")
    with api_engine.connect() as conn:
        blob = _published_bytes(conn)
    assert SENTINEL in blob, (
        "a PUBLISHED annotation did not reach any published view — the gate test cannot "
        "distinguish a working gate from an empty one"
    )


def test_the_api_role_cannot_read_the_underlying_tables(api_engine: Engine, clean_corpus):
    """Replaces the plan's manual `psql -U ...` line, which could not run: psql is not on PATH.

    Checks both tables. `annotation_revision` is the append-only history and holds every draft
    value ever written, so a grant there leaks more than `annotation` does.
    """
    for table in ("annotation", "annotation_revision"):
        with api_engine.connect() as conn:
            try:
                conn.execute(sa.text(f"SELECT * FROM {table} LIMIT 1"))
            except sa.exc.ProgrammingError as exc:
                sqlstate = getattr(exc.orig, "sqlstate", None)
                assert sqlstate == INSUFFICIENT_PRIVILEGE, (
                    f"reading {table} as the API role failed with SQLSTATE {sqlstate!r}, not "
                    f"{INSUFFICIENT_PRIVILEGE} (insufficient_privilege). A missing table and a "
                    f"denied one are different facts: {exc}"
                )
            else:
                raise AssertionError(
                    f"the API role CAN read {table}; the gate is a view over rows it can "
                    f"already see directly"
                )


@pytest.mark.parametrize("target", ["published_text", "published_verse",
                                    "annotation", "annotation_revision", "verse", "text"])
@pytest.mark.parametrize("verb", ["INSERT", "UPDATE", "DELETE"])
def test_the_api_role_cannot_WRITE_anything(api_engine: Engine, clean_corpus,
                                            target: str, verb: str):
    """M7, 2026-09-16: nothing asserted the consumer identity is read-only.

    `published_text` is a simple single-table view, which Postgres makes AUTO-UPDATABLE -- so
    a grant of INSERT/UPDATE/DELETE on it would write straight through to `text`. Today no
    write is granted and this passes, but the entire gate is grant configuration and only
    SELECT was ever pinned. An unpinned privilege is one migration away from being wrong.
    """
    stmt = {
        "INSERT": f"INSERT INTO {target} DEFAULT VALUES",
        "UPDATE": f"UPDATE {target} SET id = id",
        "DELETE": f"DELETE FROM {target}",
    }[verb]
    with api_engine.connect() as conn:
        try:
            conn.execute(sa.text(stmt))
        except sa.exc.ProgrammingError as exc:
            sqlstate = getattr(exc.orig, "sqlstate", None)
            # 42501 insufficient_privilege is the expected refusal. 42P01/42703/0A000 mean the
            # statement never got as far as a permission check (no such table/column, or the
            # view is not updatable) -- also a refusal, but for a different reason, so the
            # message says which rather than smoothing them together.
            assert sqlstate in {INSUFFICIENT_PRIVILEGE, "42P01", "42703", "0A000", "55000"}, (
                f"{verb} on {target} as the API role failed with SQLSTATE {sqlstate!r}, which "
                f"is neither a permission refusal nor a structural one: {exc}"
            )
        except sa.exc.DatabaseError as exc:
            sqlstate = getattr(exc.orig, "sqlstate", None)
            assert sqlstate is not None, f"{verb} on {target} failed opaquely: {exc}"
        else:
            raise AssertionError(
                f"the API role CAN {verb} on {target}. The consumer identity must be "
                f"read-only; a writable published view writes straight through to its base table."
            )
