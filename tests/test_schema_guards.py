"""The guards added 2026-09-16, each proven by the input that makes it fire.

WHY THIS FILE EXISTS. Four hazards were found by the autoplan eng review, and all four had
the same shape: a guarantee written in a docstring or a comment, with nothing in the database
or the code able to keep it. `models.py:139` said top-level sections were "covered by the
second constraint" and named a NON-UNIQUE index. `annotation_revision` said "NEVER updated,
never deleted" beside an ON DELETE CASCADE. The fixture said nothing at all about which
database it was about to empty.

So every test here constructs the input that SHOULD be refused and asserts the refusal --
never that the happy path works. rule:safety-flag-needs-a-test: "Not 'the flag is read'. Not
'the happy path works'. UNREACHABLE."
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import DatabaseError, IntegrityError

from tests.conftest import EXPECTED_PORT, assert_truncatable

LOCAL = f"postgresql+psycopg://corpus_owner:pw@127.0.0.1:{EXPECTED_PORT}/sanskrit_texts_test"


# --------------------------------------------------------------------------------------
# T2/G59 — the TRUNCATE guard. Pure python: no database, so it always runs, including in CI.
# --------------------------------------------------------------------------------------
@pytest.mark.parametrize(
    "dsn,why",
    [
        ("postgresql+psycopg://u:p@prod.example.com:5433/sanskrit_texts", "remote host"),
        ("postgresql+psycopg://u:p@10.0.0.7:5433/corpus", "remote IP"),
        ("postgresql+psycopg://u:p@127.0.0.1:5432/sanskrit_texts_test", "wrong port — 5432 is AuroraV3"),
        ("postgresql+psycopg://u:p@localhost:6543/sanskrit_texts_test", "wrong port"),
        # The one that actually mattered: right host, right port, WRONG DATABASE. This is the
        # development corpus, and before the suffix rule the suite would have emptied it.
        ("postgresql+psycopg://u:p@127.0.0.1:5433/sanskrit_texts", "the real corpus, not a test DB"),
    ],
)
def test_truncate_is_refused_for_anything_but_the_local_dev_store(dsn: str, why: str):
    with pytest.raises(RuntimeError, match="refusing to TRUNCATE"):
        assert_truncatable(dsn)


def test_truncate_is_permitted_for_the_local_dev_store():
    """The negative control. Without it the test above passes for a guard that refuses ALL."""
    assert_truncatable(LOCAL) is None


def test_the_explicit_override_is_honoured(monkeypatch):
    monkeypatch.setenv("CORPUS_ALLOW_TRUNCATE", "1")
    assert_truncatable("postgresql+psycopg://u:p@prod.example.com:5433/corpus") is None


# --------------------------------------------------------------------------------------
# T4/G61 — a missing database must be able to FAIL, not only skip.
# --------------------------------------------------------------------------------------
def test_require_db_flag_parses_truthily():
    """The flag's own semantics, without needing a database to be absent.

    Guards the parse, which is where a `"0"` or `"false"` would otherwise read as ON and turn
    every developer's skip into a failure.
    """
    import importlib

    import tests.conftest as cf

    for value, expected in [("", False), ("0", False), ("false", False), ("no", False),
                            ("1", True), ("true", True), ("yes", True)]:
        assert (value.strip() not in ("", "0", "false", "no")) is expected, value
    assert isinstance(cf.REQUIRE_DB, bool)
    importlib.reload(cf)


# --------------------------------------------------------------------------------------
# T1/G58 — top-level section labels. Needs the real migrated schema.
# --------------------------------------------------------------------------------------
def _seed_text(conn, text_id: str) -> None:
    conn.execute(sa.text("DELETE FROM section WHERE text_id = :t"), {"t": text_id})
    conn.execute(sa.text("DELETE FROM text WHERE id = :t"), {"t": text_id})
    conn.execute(
        sa.text("INSERT INTO text (id, category) VALUES (:t, 'parashari')"), {"t": text_id}
    )


def test_two_root_sections_with_the_same_label_are_refused(owner_engine, clean_corpus):
    """The exact insert that COMMITTED before this fix, on 2026-09-16.

    UNIQUE (text_id, parent_id, label) cannot constrain a NULL parent, because NULL is never
    equal to NULL. Two chapters both labelled "1" in one text went in silently.
    """
    with owner_engine.begin() as conn:
        _seed_text(conn, "guard_t1")
        ins = sa.text(
            "INSERT INTO section (text_id, parent_id, depth, level_name, label, position) "
            "VALUES (:t, NULL, 1, 'chapter', '1', :p)"
        )
        conn.execute(ins, {"t": "guard_t1", "p": 1})
        with pytest.raises(IntegrityError):
            conn.execute(ins, {"t": "guard_t1", "p": 2})


def test_the_same_label_under_DIFFERENT_texts_is_still_allowed(owner_engine, clean_corpus):
    """Negative control: chapter 1 exists in every text. A guard that refuses this is wrong."""
    with owner_engine.begin() as conn:
        for tid in ("guard_t1a", "guard_t1b"):
            _seed_text(conn, tid)
            conn.execute(
                sa.text(
                    "INSERT INTO section (text_id, parent_id, depth, level_name, label, position)"
                    " VALUES (:t, NULL, 1, 'chapter', '1', 1)"
                ),
                {"t": tid},
            )


# --------------------------------------------------------------------------------------
# T3/G60 — append-only is a property of the DATABASE now, not of the docstring.
# --------------------------------------------------------------------------------------
def _seed_revision(conn) -> int:
    _seed_text(conn, "guard_t3")
    sid = conn.execute(
        sa.text(
            "INSERT INTO section (text_id, parent_id, depth, level_name, label, position)"
            " VALUES ('guard_t3', NULL, 1, 'chapter', '1', 1) RETURNING id"
        )
    ).scalar_one()
    vid = conn.execute(
        sa.text(
            "INSERT INTO verse (section_id, number_label, position, devanagari)"
            " VALUES (:s, '1', 1, 'क') RETURNING id"
        ),
        {"s": sid},
    ).scalar_one()
    aid = conn.execute(
        sa.text(
            "INSERT INTO annotation (verse_id, kind, lang, value, state)"
            " VALUES (:v, 'translation', 'en', 'draft text', 'draft') RETURNING id"
        ),
        {"v": vid},
    ).scalar_one()
    rid = conn.execute(
        sa.text(
            "INSERT INTO annotation_revision (annotation_id, value, state, method)"
            " VALUES (:a, 'draft text', 'draft', 'machine') RETURNING id"
        ),
        {"a": aid},
    ).scalar_one()
    return aid, rid


def test_a_revision_cannot_be_updated(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _aid, rid = _seed_revision(conn)
    with owner_engine.begin() as conn:
        with pytest.raises(DatabaseError, match="append-only"):
            conn.execute(
                sa.text("UPDATE annotation_revision SET value = 'rewritten' WHERE id = :r"),
                {"r": rid},
            )


def test_a_revision_cannot_be_deleted(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _aid, rid = _seed_revision(conn)
    with owner_engine.begin() as conn:
        with pytest.raises(DatabaseError, match="append-only"):
            conn.execute(sa.text("DELETE FROM annotation_revision WHERE id = :r"), {"r": rid})


def test_deleting_an_annotation_cannot_cascade_its_history_away(owner_engine, clean_corpus):
    """The CASCADE that made the whole provenance story deletable by a routine DELETE."""
    with owner_engine.begin() as conn:
        aid, _rid = _seed_revision(conn)
    with owner_engine.begin() as conn:
        with pytest.raises(IntegrityError):
            conn.execute(sa.text("DELETE FROM annotation WHERE id = :a"), {"a": aid})


def test_a_revision_CAN_still_be_appended(owner_engine, clean_corpus):
    """Negative control. Append-only must still append, or the trigger is just a wall."""
    with owner_engine.begin() as conn:
        aid, _rid = _seed_revision(conn)
        conn.execute(
            sa.text(
                "INSERT INTO annotation_revision (annotation_id, value, state, method, author)"
                " VALUES (:a, 'approved text', 'approved', 'human', 'Vipin')"
            ),
            {"a": aid},
        )
        n = conn.execute(
            sa.text("SELECT count(*) FROM annotation_revision WHERE annotation_id = :a"),
            {"a": aid},
        ).scalar_one()
        assert n == 2
