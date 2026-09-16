"""Two checks that were written down as prose and never made mechanical.

WHY THIS FILE EXISTS (M3). The migration ends with
`ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM corpus_api` and calls
itself "belt and braces". It is neither. Default-privilege REVOKE only removes a default
*grant* for objects created after it runs, and no default grant to `corpus_api` was ever
established for it to remove — Postgres does not grant a fresh table's privileges to anyone
but its owner unless a default-privilege *GRANT* said otherwise, and this migration never
issued one. The statement executes, changes nothing, and reads as protection.
`rule:discernment-checks` §1: a check that cannot fail is worse than no check. The real hazard
it was trying to name is a *future* migration writing an explicit
`GRANT ... TO corpus_api` or `TO PUBLIC` — which nothing here would catch. That is what
`test_corpus_api_grant_set_is_exactly_select_on_published_views` below actually catches, by
reading the grant catalog rather than trusting a REVOKE that never had anything to revoke.

WHY THIS FILE EXISTS (M8). `published_verse` is
`verse LEFT JOIN section JOIN text LEFT JOIN annotation ... AND a.state='approved'` — a LEFT
JOIN that fans out one row per approved annotation, plus one NULL-annotation row for a verse
with none. Nobody wrote that down as a contract, so a first consumer gets two things wrong for
free: `count(*)` is an annotation count, not a verse count, and a verse holding only drafts is
byte-identical in the view to a verse holding nothing at all. The tests below PIN that
behaviour — they do not redesign the view, and they will go red the day someone changes the
join without meaning to change what it promises.
"""

from __future__ import annotations

import sqlalchemy as sa
from sqlalchemy.engine import Engine

from tests.test_publication_gate import published_views

# --------------------------------------------------------------------------------------
# M3 — the grant set, read from the catalog, never from a hardcoded list of views.
# --------------------------------------------------------------------------------------


def test_corpus_api_grant_set_is_exactly_select_on_published_views(
    owner_engine: Engine, clean_corpus
):
    """The check the inert `ALTER DEFAULT PRIVILEGES` line in 0001 cannot be.

    Expected is DERIVED from `information_schema.views` (via `published_views`, the same
    G17-fixed helper `test_publication_gate.py` uses), never a literal `{"published_text",
    "published_verse"}` tuple — a view added to the migration tomorrow must appear on both
    sides of this comparison or the test is checking a snapshot of today, not the schema.

    Read with `owner_engine` (superuser) so the query sees every grant regardless of who
    issued it — this is a catalog inspection, not a leak-of-data test, so there is no reason
    to read it as the constrained consumer.
    """
    with owner_engine.connect() as conn:
        expected = {(view, "SELECT") for view in published_views(conn)}
        actual = set(
            conn.execute(
                sa.text(
                    "SELECT table_name, privilege_type FROM information_schema.role_table_grants "
                    "WHERE grantee = 'corpus_api'"
                )
            ).all()
        )
    assert actual == expected, (
        f"corpus_api's grant set drifted from the published views.\n"
        f"  expected (derived from information_schema.views): {expected}\n"
        f"  actual   (from information_schema.role_table_grants): {actual}\n"
        f"  extra: {actual - expected}\n"
        f"  missing: {expected - actual}\n"
        "A grant appearing here that isn't SELECT on a published view is exactly the hazard "
        "the migration's inert ALTER DEFAULT PRIVILEGES line was meant to catch and cannot."
    )


# --------------------------------------------------------------------------------------
# M8 — published_verse's grain, pinned rather than assumed.
# --------------------------------------------------------------------------------------


def _seed_grain_text(conn: sa.Connection, text_id: str) -> dict[str, int]:
    """One text, one chapter, three verses exercising the three grain cases:

      v_two_approved   -- two APPROVED annotations (en + hi translation)  -> 2 rows
      v_unannotated    -- no annotation row at all                        -> 1 NULL row
      v_draft_only     -- one annotation, state='draft' (never approved)  -> 1 NULL row,
                           and it must be indistinguishable from v_unannotated's row
    """
    conn.execute(sa.text("DELETE FROM section WHERE text_id = :t"), {"t": text_id})
    conn.execute(sa.text("DELETE FROM text WHERE id = :t"), {"t": text_id})
    conn.execute(
        sa.text("INSERT INTO text (id, category) VALUES (:t, 'parashari')"), {"t": text_id}
    )
    sid = conn.execute(
        sa.text(
            "INSERT INTO section (text_id, parent_id, depth, level_name, label, position)"
            " VALUES (:t, NULL, 1, 'chapter', '1', 1) RETURNING id"
        ),
        {"t": text_id},
    ).scalar_one()

    verse_ids: dict[str, int] = {}
    for label, position in (("v_two_approved", 1), ("v_unannotated", 2), ("v_draft_only", 3)):
        vid = conn.execute(
            sa.text(
                "INSERT INTO verse (section_id, number_label, position, devanagari)"
                " VALUES (:s, :n, :p, 'क') RETURNING id"
            ),
            {"s": sid, "n": str(position), "p": position},
        ).scalar_one()
        verse_ids[label] = vid

    conn.execute(
        sa.text(
            "INSERT INTO annotation (verse_id, kind, lang, value, state)"
            " VALUES (:v, 'translation', 'en', 'the meaning', 'approved')"
        ),
        {"v": verse_ids["v_two_approved"]},
    )
    conn.execute(
        sa.text(
            "INSERT INTO annotation (verse_id, kind, lang, value, state)"
            " VALUES (:v, 'translation', 'hi', 'अर्थ', 'approved')"
        ),
        {"v": verse_ids["v_two_approved"]},
    )
    # v_unannotated gets nothing at all.
    conn.execute(
        sa.text(
            "INSERT INTO annotation (verse_id, kind, lang, value, state)"
            " VALUES (:v, 'translation', 'en', 'not yet reviewed', 'draft')"
        ),
        {"v": verse_ids["v_draft_only"]},
    )
    return verse_ids


def _rows_for(conn: sa.Connection, verse_id: int) -> list[sa.Row]:
    return conn.execute(
        sa.text("SELECT * FROM published_verse WHERE verse_id = :v ORDER BY lang NULLS FIRST"),
        {"v": verse_id},
    ).mappings().all()


def test_a_verse_with_two_approved_annotations_yields_two_rows(
    owner_engine: Engine, api_engine: Engine, clean_corpus
):
    """The fan-out half of the grain: the view is one row per approved annotation, not one
    row per verse. A consumer treating `published_verse` as verse-grained double-counts here.
    """
    with owner_engine.begin() as conn:
        verse_ids = _seed_grain_text(conn, "grain_fanout")
    with api_engine.connect() as conn:
        rows = _rows_for(conn, verse_ids["v_two_approved"])
    assert len(rows) == 2, f"expected one row per approved annotation, got {len(rows)}: {rows}"
    langs = {r["lang"] for r in rows}
    assert langs == {"en", "hi"}, f"expected both approved translations present, got {langs}"


def test_an_unannotated_verse_still_produces_exactly_one_row_with_null_annotation_columns(
    owner_engine: Engine, api_engine: Engine, clean_corpus
):
    """The LEFT JOIN's other half: a verse with zero annotation rows is not absent from
    `published_verse` — it is present once, with `kind`/`lang`/`value` all NULL. A consumer
    doing `SELECT count(*) ... GROUP BY verse_id` would read this as "one translation."
    """
    with owner_engine.begin() as conn:
        verse_ids = _seed_grain_text(conn, "grain_unannotated")
    with api_engine.connect() as conn:
        rows = _rows_for(conn, verse_ids["v_unannotated"])
    assert len(rows) == 1, f"expected exactly one NULL-annotation row, got {len(rows)}: {rows}"
    row = rows[0]
    assert row["kind"] is None and row["lang"] is None and row["value"] is None, (
        f"an unannotated verse's row must carry NULL kind/lang/value, got {dict(row)}"
    )


def test_a_verse_with_only_a_draft_is_indistinguishable_from_an_unannotated_verse(
    owner_engine: Engine, api_engine: Engine, clean_corpus
):
    """The consequence that will actually bite someone: a verse holding a draft that nobody
    has approved yet produces the SAME row, byte for byte on every published column, as a
    verse holding nothing. This is not a bug to fix here — it is the structural gate working
    as designed (a draft has no path to a consumer) — but it means "no translation shown"
    can mean either "untranslated" or "translated and awaiting review", and the view alone
    cannot tell a caller which. Pinned so that fact cannot change silently.
    """
    with owner_engine.begin() as conn:
        verse_ids = _seed_grain_text(conn, "grain_draft_only")
    with api_engine.connect() as conn:
        draft_rows = _rows_for(conn, verse_ids["v_draft_only"])
        blank_rows = _rows_for(conn, verse_ids["v_unannotated"])
    assert len(draft_rows) == 1, (
        f"a draft-only verse must still surface exactly one row, got {len(draft_rows)}"
    )
    # Compare every column except the identifying keys (verse_id/text_id/section_id differ
    # because these are two different verses) — the ANNOTATION-shaped columns must match.
    annotation_cols = ("kind", "lang", "value")
    draft_annotation = {c: draft_rows[0][c] for c in annotation_cols}
    blank_annotation = {c: blank_rows[0][c] for c in annotation_cols}
    assert draft_annotation == blank_annotation == {"kind": None, "lang": None, "value": None}, (
        "a draft-only verse and a genuinely unannotated verse must be byte-identical on the "
        f"annotation columns; draft={draft_annotation} unannotated={blank_annotation}"
    )


def test_count_star_over_published_verse_is_an_annotation_count_not_a_verse_count(
    owner_engine: Engine, api_engine: Engine, clean_corpus
):
    """Names the exact mistake a first consumer will make: `SELECT count(*) FROM
    published_verse WHERE text_id = ...` is not "how many verses does this text have."

    This text has 3 verses (one with 2 approved annotations, one with none, one with a draft
    only) so a verse count would be 3 -- but `published_verse` emits 4 rows for it.
    """
    with owner_engine.begin() as conn:
        _seed_grain_text(conn, "grain_count")
    with api_engine.connect() as conn:
        n_rows = conn.execute(
            sa.text("SELECT count(*) FROM published_verse WHERE text_id = :t"),
            {"t": "grain_count"},
        ).scalar_one()
        n_distinct_verses = conn.execute(
            sa.text("SELECT count(DISTINCT verse_id) FROM published_verse WHERE text_id = :t"),
            {"t": "grain_count"},
        ).scalar_one()
    assert n_distinct_verses == 3, f"the text was seeded with 3 verses, got {n_distinct_verses}"
    assert n_rows == 4, (
        f"expected 4 rows (2 for v_two_approved + 1 for v_unannotated + 1 for v_draft_only), "
        f"got {n_rows}"
    )
    assert n_rows != n_distinct_verses, (
        "count(*) happened to equal the verse count for this fixture, which would hide the "
        "grain mismatch this test exists to pin -- the fixture needs a verse with >1 approved "
        "annotation to make the two numbers diverge"
    )
