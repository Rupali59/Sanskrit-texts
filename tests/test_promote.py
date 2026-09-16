"""§6's acceptance test: promotion without a named reviewer FAILS.

This is the one requirement the review mechanism was declared a hard blocker for. Everything
else about the editorial lifecycle is convenience; this is the property the publication gate
rests on, and the reason D9's `translated -> published` mapping was withdrawn before it ran.

Each test constructs the promotion that must be refused and asserts the refusal -- never that
the happy path works. The happy path has one test, as the negative control, because a guard
that refuses everything passes every refusal test.
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa

from sanskrit_texts.promote import TRANSITIONS, PromotionRefused, promote


def _seed(conn: sa.Connection, *, state: str = "draft", n: int = 2) -> None:
    conn.execute(sa.text(
        "INSERT INTO text (id, category, source_sha) VALUES ('promo', 'parashari', 'x')"))
    conn.execute(sa.text(
        "INSERT INTO section (id, text_id, parent_id, depth, level_name, label, position)"
        " VALUES (1, 'promo', NULL, 1, 'chapter', '1', 1)"))
    for i in range(1, n + 1):
        conn.execute(
            sa.text("INSERT INTO verse (id, section_id, number_label, position, devanagari)"
                    " VALUES (:i, 1, :l, :i, 'अथ')"), {"i": i, "l": str(i)})
        conn.execute(
            sa.text("INSERT INTO annotation (id, verse_id, kind, lang, value, state,"
                    " source_field) VALUES (:i, :i, 'translation', 'en', :v, :s, 'english')"),
            {"i": i, "v": f"translation {i}", "s": state})


def test_approving_without_an_author_is_refused(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _seed(conn)
        with pytest.raises(PromotionRefused, match="requires --author"):
            promote(conn, text_id="promo", to_state="approved", author=None)


@pytest.mark.parametrize("author", ["", "   ", None])
def test_a_blank_author_is_not_an_author(owner_engine, clean_corpus, author):
    """Whitespace is the obvious way round a truthiness check, so it gets its own case."""
    with owner_engine.begin() as conn:
        _seed(conn)
        with pytest.raises(PromotionRefused, match="requires --author"):
            promote(conn, text_id="promo", to_state="approved", author=author)


@pytest.mark.parametrize("method", ["machine", "matcher"])
def test_only_a_human_may_approve(owner_engine, clean_corpus, method):
    with owner_engine.begin() as conn:
        _seed(conn)
        with pytest.raises(PromotionRefused, match="requires --method human"):
            promote(conn, text_id="promo", to_state="approved", author="Vipin", method=method)


def test_a_matcher_MAY_move_something_into_review(owner_engine, clean_corpus):
    """The other half: non-human methods are not banned, they are banned from `approved`."""
    with owner_engine.begin() as conn:
        _seed(conn)
        moved = promote(conn, text_id="promo", to_state="in_review", author=None,
                        method="matcher")
        assert moved == 2


def test_matching_nothing_is_refused_rather_than_reported_as_success(owner_engine,
                                                                     clean_corpus):
    """rule:discernment-checks §2 -- 'looked at nothing' and 'found nothing' differ."""
    with owner_engine.begin() as conn:
        _seed(conn)
        with pytest.raises(PromotionRefused, match="no annotation matched"):
            promote(conn, text_id="does-not-exist", to_state="in_review", author=None)


def test_an_illegal_transition_is_refused(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _seed(conn, state="draft")
        with pytest.raises(PromotionRefused, match="illegal transition"):
            promote(conn, text_id="promo", to_state="superseded", author=None)


def test_superseded_is_terminal():
    """Stated as a property of the table, so a future edit that adds an exit is deliberate."""
    assert TRANSITIONS["superseded"] == set()


def test_a_named_human_CAN_approve_and_the_revision_records_them(owner_engine, clean_corpus):
    """The negative control, plus the audit trail that makes bulk promotion defensible."""
    with owner_engine.begin() as conn:
        _seed(conn)
        moved = promote(conn, text_id="promo", to_state="approved", author="Vipin Kaushik",
                        note="accepted unchanged after reading")
        assert moved == 2
        states = conn.execute(sa.text("SELECT DISTINCT state FROM annotation")).scalars().all()
        assert states == ["approved"]
        rev = conn.execute(sa.text(
            "SELECT author, method, state, note FROM annotation_revision"
            " WHERE state = 'approved'")).mappings().all()
        assert len(rev) == 2
        assert {r["author"] for r in rev} == {"Vipin Kaushik"}
        assert {r["method"] for r in rev} == {"human"}
        assert {r["note"] for r in rev} == {"accepted unchanged after reading"}


def test_approving_TWO_candidates_for_one_verse_is_refused(owner_engine, clean_corpus):
    """A verse commonly holds both a served value and its draft -- 2,369 do.

    Approving "the verse" is then ambiguous: which of the two becomes the approved one? The
    partial unique index permits exactly one, so reaching it would abort the whole promotion
    with a constraint error. Naming the clash is more useful, and it makes explicit that
    approving is a CHOICE between candidates rather than a bulk operation.
    """
    with owner_engine.begin() as conn:
        _seed(conn, n=1)
        conn.execute(sa.text(
            "INSERT INTO annotation (id, verse_id, kind, lang, value, state, source_field)"
            " VALUES (99, 1, 'translation', 'en', 'a better translation', 'draft',"
            " 'english_draft')"))
        with pytest.raises(PromotionRefused, match="more than one approved value"):
            promote(conn, text_id="promo", to_state="approved", author="Vipin")


def test_a_later_approval_supersedes_the_earlier_one(owner_engine, clean_corpus):
    """The genuine supersede path: approve one, then approve a DIFFERENT one later.

    Without the supersede step the second UPDATE violates the partial unique index and the
    promotion aborts, so this is correctness rather than housekeeping.
    """
    with owner_engine.begin() as conn:
        _seed(conn, n=1)
        promote(conn, text_id="promo", to_state="approved", author="Vipin")
        conn.execute(sa.text(
            "INSERT INTO annotation (id, verse_id, kind, lang, value, state, source_field)"
            " VALUES (99, 1, 'translation', 'en', 'a better translation', 'draft',"
            " 'english_draft')"))
        promote(conn, text_id="promo", to_state="approved", author="Vipin", kind="translation",
                lang="en")
        rows = dict(conn.execute(sa.text(
            "SELECT id, state FROM annotation ORDER BY id")).all())
        assert rows == {1: "superseded", 99: "approved"}, rows
