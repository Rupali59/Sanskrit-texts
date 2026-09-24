"""T6 Phase A -- confidence markers on translations and tags.

TWO LAYERS, TWO KINDS OF TEST.

The MACHINE layer (`sanskrit_texts.checks`) is pure: `check_translation`, `check_tag` and
`find_duplicate_tag_ids` take plain values and return `(level, reasons)`, so most of this file
needs no database at all -- one fixture per reason, plus a clean value that must resolve to
`no-defect-found` (rule:discernment-checks §1: a check that cannot fail ships with its failing
input, and the mirror of that is a check that cannot PASS ships with its clean one).

The HUMAN layer (`promote.py --confidence`, and `annotation_revision`'s CHECK constraints)
needs the real migrated schema, so those tests use `owner_engine`/`api_engine` like every
other DB test in this suite.

THE INVARIANT test is the one that matters most: a machine check must never change
`annotation.state` or reach a published view. See its docstring for the mutation proof.
"""

from __future__ import annotations

import pytest
import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sanskrit_texts.checks import (
    check_tag,
    check_translation,
    compute_checks,
    find_duplicate_tag_ids,
    iter_annotation_rows,
    upsert_checks,
)
from sanskrit_texts.promote import CONFIDENCES, PromotionRefused, promote
from tests.test_publication_gate import SENTINEL, _published_bytes

# ----------------------------------------------------------------------------------------
# Pure fixtures: check_translation. One per reason, plus a clean value for each language.
# ----------------------------------------------------------------------------------------


def test_template_prefix_fails():
    level, reasons = check_translation(
        "en", "Classical text translation of BPHS 1.1: the sun rises", "अथ श्री गणेशाय नमः"
    )
    assert level == "fails"
    assert "template-prefix" in reasons


def test_sanskrit_echo_in_an_english_translation_fails():
    """Overwhelmingly Devanagari, with one Latin letter so `wrong-script` does not also fire
    -- isolating the reason this fixture exists for."""
    level, reasons = check_translation("en", "अथातो धर्मजिज्ञासा X", "किंचित्")
    assert level == "fails"
    assert "sanskrit-echo" in reasons
    assert "wrong-script" not in reasons


def test_wrong_script_english_with_zero_latin_letters_fails():
    """Neither Latin nor Devanagari, so `sanskrit-echo` (a Devanagari-share measure) cannot
    also fire -- this isolates `wrong-script` alone."""
    level, reasons = check_translation("en", "αβγδεζη", "किंचित्")
    assert level == "fails"
    assert "wrong-script" in reasons
    assert "sanskrit-echo" not in reasons


def test_sanskrit_echo_hindi_exact_match_fails():
    dev = "अथातो धर्मजिज्ञासा"
    level, reasons = check_translation("hi", dev, dev)
    assert level == "fails"
    assert "sanskrit-echo" in reasons


def test_sanskrit_echo_hindi_contains_first_40_chars_fails():
    dev = "अथातो धर्मजिज्ञासा " * 3  # > 40 characters
    value = "एक अनुवाद: " + dev[:40] + " शेष"
    level, reasons = check_translation("hi", value, dev)
    assert level == "fails"
    assert "sanskrit-echo" in reasons


def test_short_sanskrit_hindi_gloss_containing_the_term_is_not_an_echo():
    """Regression for the false-positive class in `quiet-juggling-cherny` Lane D. Below
    `_SANSKRIT_ECHO_MIN_LEN`, `stripped_dev[:40]` used to be the WHOLE Sanskrit, so the
    containment check degenerated into "mentions the term at all" -- a correct gloss that
    quotes a short term legitimately does. Live example: `bhrigu_sutram` ch3 v37."""
    dev = "मायावादी"
    hindi = "वह मायावादी (भ्रम में विश्वास रखने वाला या छल करने वाला) होगा।"
    level, reasons = check_translation("hi", hindi, dev)
    assert "sanskrit-echo" not in reasons
    assert level == "no-defect-found"


def test_long_sanskrit_genuinely_echoed_into_hindi_still_fails():
    """The fix is scoped to short Sanskrit only -- it must not blunt the real defect class
    (`astanga_hridaya`, 18 live hits, Sanskrit well over the threshold)."""
    dev = "श्री गणेशाय नमः तस्मात् सर्वप्रयत्नेन " * 3  # > 40 characters
    value = "हिन्दी में: " + dev[:40] + " आगे"
    level, reasons = check_translation("hi", value, dev)
    assert level == "fails"
    assert "sanskrit-echo" in reasons


def test_wrong_script_hindi_with_zero_devanagari_fails():
    level, reasons = check_translation("hi", "this is plain english text", "किंचित्")
    assert level == "fails"
    assert "wrong-script" in reasons


def test_too_short_relative_to_a_long_sanskrit_verse_is_suspect():
    dev = "क" * 60  # > 40 chars, so the ratio check applies
    level, reasons = check_translation("en", "the meaning", dev)  # well under 0.3 * 60 = 18
    assert level == "suspect"
    assert reasons == ["too-short"]


def test_a_short_sanskrit_verse_never_triggers_too_short():
    """The threshold is gated on the SANSKRIT being long enough to be short RELATIVE to --
    without this, every terse but complete translation of a terse verse would flag."""
    level, reasons = check_translation("en", "om", "ॐ")
    assert level == "no-defect-found"
    assert reasons == []


def test_not_nfc_is_suspect():
    decomposed = "café"  # e + COMBINING ACUTE ACCENT, not the precomposed é
    assert decomposed != __import__("unicodedata").normalize("NFC", decomposed)
    level, reasons = check_translation("en", decomposed, "किंचित्")
    assert level == "suspect"
    assert reasons == ["not-nfc"]


def test_a_clean_english_translation_is_no_defect_found():
    level, reasons = check_translation(
        "en", "a plain english translation of the verse", "अथातो धर्मजिज्ञासा"
    )
    assert level == "no-defect-found"
    assert reasons == []


def test_a_clean_hindi_translation_is_no_defect_found():
    level, reasons = check_translation("hi", "एक सामान्य हिंदी अनुवाद", "अथातो धर्मजिज्ञासा")
    assert level == "no-defect-found"
    assert reasons == []


@pytest.mark.parametrize(
    "lang,value,devanagari",
    [
        ("en", "Classical text translation of X: y", "अ"),
        ("en", "अथातो धर्मजिज्ञासा X", "अ"),
        ("en", "αβγδεζη", "अ"),
        ("hi", "अथातो", "अथातो"),
        ("en", "café", "अ"),
    ],
)
def test_a_check_never_reports_unchecked(lang, value, devanagari):
    """`unchecked` is legal in the CHECK constraint for completeness only -- checks.py must
    never emit it itself; a row simply absent from `annotation_check` IS "never checked"."""
    level, _reasons = check_translation(lang, value, devanagari)
    assert level != "unchecked"


# ----------------------------------------------------------------------------------------
# Pure fixtures: check_tag and find_duplicate_tag_ids.
# ----------------------------------------------------------------------------------------


def test_malformed_tag_with_no_colon_fails():
    level, reasons = check_tag("not-a-tag-at-all")
    assert level == "fails"
    assert reasons == ["malformed-tag"]


def test_malformed_tag_with_an_uppercase_namespace_fails():
    """Uppercase does not match the `ns:value` shape at all -- this is malformed, not merely
    an unknown namespace, and the two must stay distinguishable reasons."""
    level, reasons = check_tag("GRAHA:jupiter")
    assert level == "fails"
    assert reasons == ["malformed-tag"]


def test_unknown_namespace_fails():
    level, reasons = check_tag("foobar:mars")
    assert level == "fails"
    assert reasons == ["unknown-namespace"]


def test_a_clean_tag_is_no_defect_found():
    level, reasons = check_tag("graha:jupiter")
    assert level == "no-defect-found"
    assert reasons == []


def test_find_duplicate_tag_ids_flags_only_the_repeated_value():
    rows = [(1, "graha:jupiter"), (2, "graha:jupiter"), (3, "bhava:8")]
    assert find_duplicate_tag_ids(rows) == {1, 2}


def test_compute_checks_folds_duplicate_tag_into_the_per_annotation_result():
    """Through the assembly function, not just the standalone helper -- `duplicate-tag` must
    reach the SAME dict `check_tag` populated, escalating a clean tag to `suspect`."""
    rows = [
        {"annotation_id": 1, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "graha:jupiter", "state": "draft", "devanagari": "अ"},
        {"annotation_id": 2, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "graha:jupiter", "state": "draft", "devanagari": "अ"},
        {"annotation_id": 3, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "bhava:8", "state": "draft", "devanagari": "अ"},
    ]
    results = compute_checks(rows)
    assert results[1] == ("suspect", ["duplicate-tag"])
    assert results[2] == ("suspect", ["duplicate-tag"])
    assert results[3] == ("no-defect-found", [])


def test_a_duplicate_that_is_ALSO_malformed_stays_fails_not_downgraded_to_suspect():
    """`add_reason` must never downgrade severity -- a duplicate of two malformed tags is
    still `fails`, with both reasons recorded."""
    rows = [
        {"annotation_id": 1, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "not-a-tag", "state": "draft", "devanagari": "अ"},
        {"annotation_id": 2, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "not-a-tag", "state": "draft", "devanagari": "अ"},
    ]
    results = compute_checks(rows)
    assert results[1] == ("fails", ["duplicate-tag", "malformed-tag"])
    assert results[2] == ("fails", ["duplicate-tag", "malformed-tag"])


def test_duplicate_tag_is_scoped_to_one_verse_and_state_not_the_whole_corpus():
    rows = [
        {"annotation_id": 1, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "graha:jupiter", "state": "draft", "devanagari": "अ"},
        {"annotation_id": 2, "verse_id": 11, "kind": "tag", "lang": None,
         "value": "graha:jupiter", "state": "draft", "devanagari": "अ"},
        {"annotation_id": 3, "verse_id": 10, "kind": "tag", "lang": None,
         "value": "graha:jupiter", "state": "approved", "devanagari": "अ"},
    ]
    results = compute_checks(rows)
    # Different verse, and a different STATE on the same verse, are both different groups --
    # none of these three collide with any other.
    assert all(reasons == [] for _level, reasons in results.values())


# ----------------------------------------------------------------------------------------
# DB fixtures shared by the tests below.
# ----------------------------------------------------------------------------------------


def _seed_translations(
    conn: sa.Connection, *, text_id: str = "conf", n: int = 1,
    devanagari: str = "अ", value_prefix: str = "translation",
) -> list[int]:
    conn.execute(sa.text(
        "INSERT INTO text (id, category, source_sha) VALUES (:t, 'parashari', 'x')"),
        {"t": text_id})
    conn.execute(sa.text(
        "INSERT INTO section (id, text_id, parent_id, depth, level_name, label, position)"
        " VALUES (1, :t, NULL, 1, 'chapter', '1', 1)"), {"t": text_id})
    ids: list[int] = []
    for i in range(1, n + 1):
        conn.execute(sa.text(
            "INSERT INTO verse (id, section_id, number_label, position, devanagari)"
            " VALUES (:i, 1, :l, :i, :d)"), {"i": i, "l": str(i), "d": devanagari})
        conn.execute(sa.text(
            "INSERT INTO annotation (id, verse_id, kind, lang, value, state, source_field)"
            " VALUES (:i, :i, 'translation', 'en', :v, 'draft', 'english')"),
            {"i": i, "v": f"{value_prefix} {i}"})
        ids.append(i)
    return ids


def _mark_check(conn: sa.Connection, annotation_id: int, level: str,
                 reasons: list[str] | None = None) -> None:
    conn.execute(sa.text(
        "INSERT INTO annotation_check (annotation_id, level, reasons, checker_version)"
        " VALUES (:a, :l, :r, 'test')"),
        {"a": annotation_id, "l": level, "r": list(reasons or [])})


# ----------------------------------------------------------------------------------------
# Idempotence: run the CLI's own compute + upsert twice, compare table contents.
# ----------------------------------------------------------------------------------------


def test_checks_are_idempotent(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _seed_translations(conn, n=3, devanagari="क" * 60, value_prefix="short")
        conn.execute(sa.text(
            "INSERT INTO verse (id, section_id, number_label, position, devanagari)"
            " VALUES (100, 1, '100', 100, 'अ')"))
        conn.execute(sa.text(
            "INSERT INTO annotation (id, verse_id, kind, lang, value, state)"
            " VALUES (101, 100, 'tag', NULL, 'graha:jupiter', 'draft'),"
            "        (102, 100, 'tag', NULL, 'graha:jupiter', 'draft')"
        ))

    def _run() -> list[dict]:
        with owner_engine.begin() as conn:
            rows = iter_annotation_rows(conn, ["conf"])
            results = compute_checks(rows)
            upsert_checks(conn, results)
            return [
                dict(r) for r in conn.execute(sa.text(
                    "SELECT annotation_id, level, reasons, checker_version"
                    " FROM annotation_check ORDER BY annotation_id"
                )).mappings().all()
            ]

    first = _run()
    second = _run()
    # checked_at is deliberately excluded from both queries above: it is now() on every
    # write (upsert_checks's docstring), so it is NOT part of the "content" this test pins.
    assert first == second
    assert len(first) == 5  # 3 translations + 2 tags
    by_id = {r["annotation_id"]: r for r in first}
    assert by_id[1]["level"] == "suspect" and by_id[1]["reasons"] == ["too-short"]
    assert by_id[101]["level"] == "suspect" and by_id[101]["reasons"] == ["duplicate-tag"]
    assert by_id[102]["level"] == "suspect" and by_id[102]["reasons"] == ["duplicate-tag"]
    assert all(r["checker_version"] == "1" for r in first)


# ----------------------------------------------------------------------------------------
# THE INVARIANT: a check can never change annotation.state or reach a published view.
# ----------------------------------------------------------------------------------------


def test_a_check_can_never_change_state_or_reach_a_published_view(
    owner_engine, api_engine, clean_corpus
):
    """T6's invariant. Recomputing a check -- even to `no-defect-found`, the best a check can
    ever report (G55) -- must never change `annotation.state` and must never make a row appear
    in a published view. This is D9's withdrawn failure (a review recorded that never
    happened) arriving by a new route.

    MUTATION PROOF (performed by hand against this exact test, then reverted -- the red output
    is quoted verbatim in the task report, not re-created here as a permanent self-mutating
    test, because the unsafe path lives in application code (`checks.upsert_checks`), not in a
    Python-metadata object `test_schema_drift.py`'s style of in-process mutation can reach):
    a line was added to `upsert_checks` that also ran
    `UPDATE annotation SET state = 'approved' WHERE id = :id` whenever the computed level was
    `no-defect-found`. Running exactly this test then failed the `state == 'draft'` assertion
    below, for the stated reason. Reverted before commit; the mutated file's hash was compared
    before and after to confirm the mutation actually applied (a `sed` that matches nothing
    proves nothing).
    """
    with owner_engine.begin() as conn:
        aid = _seed_translations(conn, devanagari="अ", value_prefix=SENTINEL)[0]
        row = conn.execute(sa.text(
            "SELECT a.kind, a.lang, a.value, a.verse_id, a.state, v.devanagari"
            " FROM annotation a JOIN verse v ON v.id = a.verse_id WHERE a.id = :a"),
            {"a": aid}).mappings().one()
        results = compute_checks([{**row, "annotation_id": aid}])
        # A check that cannot fail is worse than no check (rule:discernment-checks §1) --
        # confirm this fixture really is clean before trusting what follows.
        level, reasons = results[aid]
        assert level == "no-defect-found", (level, reasons)

        upsert_checks(conn, results)

        state = conn.execute(sa.text(
            "SELECT state FROM annotation WHERE id = :a"), {"a": aid}).scalar_one()
        assert state == "draft", "a check upsert changed annotation.state -- the T6 invariant"

    with api_engine.connect() as conn:
        blob = _published_bytes(conn)
    assert SENTINEL not in blob, (
        "an unapproved annotation's bytes reached a published view after a check ran"
    )


# ----------------------------------------------------------------------------------------
# promote.py: --confidence and --override-reason.
# ----------------------------------------------------------------------------------------


def test_approving_without_confidence_is_refused(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _seed_translations(conn)
        with pytest.raises(PromotionRefused, match="requires --confidence"):
            promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik")


@pytest.mark.parametrize("confidence", ["", "   "])
def test_a_blank_confidence_is_not_a_confidence(owner_engine, clean_corpus, confidence):
    with owner_engine.begin() as conn:
        _seed_translations(conn)
        with pytest.raises(PromotionRefused, match="requires --confidence"):
            promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                    confidence=confidence)


def test_an_unknown_confidence_value_is_refused(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        _seed_translations(conn)
        with pytest.raises(PromotionRefused, match="unknown confidence"):
            promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                    confidence="very-sure")


def test_confidence_is_not_required_outside_approval(owner_engine, clean_corpus):
    """The other half: confidence is an `approved`-only requirement, not a global one."""
    with owner_engine.begin() as conn:
        _seed_translations(conn)
        moved = promote(conn, text_id="conf", to_state="in_review", author=None, method="matcher")
        assert moved == 1


def test_approving_a_failing_item_without_an_override_reason_is_refused(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        _mark_check(conn, ids[0], "fails", ["wrong-script"])
        with pytest.raises(PromotionRefused, match="requires --override-reason"):
            promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                    confidence="tentative")


def test_approving_a_failing_item_with_an_override_reason_succeeds_and_records_both(
    owner_engine, clean_corpus
):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        _mark_check(conn, ids[0], "fails", ["wrong-script"])
        moved = promote(
            conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
            confidence="probable", override_reason="checked by hand, translation is correct",
        )
        assert moved == 1
        rev = conn.execute(sa.text(
            "SELECT confidence, override_reason FROM annotation_revision"
            " WHERE state = 'approved'")).mappings().one()
        assert rev["confidence"] == "probable"
        assert rev["override_reason"] == "checked by hand, translation is correct"


def test_a_clean_item_needs_no_override_reason(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        _mark_check(conn, ids[0], "no-defect-found", [])
        moved = promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                        confidence="certain")
        assert moved == 1


def test_unchecked_annotations_are_allowed_and_the_count_is_reported(owner_engine, clean_corpus):
    """docs/DATABASE.md: 'unchecked annotations are allowed but the count is printed.'"""
    with owner_engine.begin() as conn:
        _seed_translations(conn, n=2)
        # Neither annotation has a row in annotation_check at all.
        result = promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                         confidence="tentative")
        assert result == 2
        assert result.unchecked == 2


def test_a_checked_item_is_not_counted_as_unchecked(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn, n=2)
        _mark_check(conn, ids[0], "no-defect-found", [])
        result = promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                         confidence="tentative")
        assert result == 2
        assert result.unchecked == 1


# ----------------------------------------------------------------------------------------
# DB CHECK: an approved revision with no confidence is refused at the database, not just by
# promote.py's Python validation.
# ----------------------------------------------------------------------------------------


def test_db_check_refuses_an_approved_revision_with_null_confidence(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
    with owner_engine.begin() as conn:
        with pytest.raises(IntegrityError, match="ck_revision_approved_has_confidence"):
            conn.execute(sa.text(
                "INSERT INTO annotation_revision (annotation_id, value, state, method, author)"
                " VALUES (:a, 'x', 'approved', 'human', 'Vipin Kaushik')"), {"a": ids[0]})


def test_db_check_refuses_an_unknown_confidence_value(owner_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
    with owner_engine.begin() as conn:
        with pytest.raises(IntegrityError, match="ck_revision_confidence"):
            conn.execute(sa.text(
                "INSERT INTO annotation_revision"
                " (annotation_id, value, state, method, author, confidence)"
                " VALUES (:a, 'x', 'in_review', 'human', 'Vipin Kaushik', 'very-sure')"),
                {"a": ids[0]})


def test_db_check_permits_an_approved_revision_with_a_valid_confidence(owner_engine, clean_corpus):
    """Negative control -- without it the two tests above could be passing because the CHECK
    refuses every insert, not because it refuses the specific bad ones."""
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        conn.execute(sa.text(
            "INSERT INTO annotation_revision"
            " (annotation_id, value, state, method, author, confidence)"
            " VALUES (:a, 'x', 'approved', 'human', 'Vipin Kaushik', 'certain')"), {"a": ids[0]})


@pytest.mark.parametrize("confidence", CONFIDENCES)
def test_every_declared_confidence_value_is_accepted(owner_engine, clean_corpus, confidence):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        conn.execute(sa.text(
            "INSERT INTO annotation_revision"
            " (annotation_id, value, state, method, author, confidence)"
            " VALUES (:a, 'x', 'approved', 'human', 'Vipin Kaushik', :c)"),
            {"a": ids[0], "c": confidence})


# ----------------------------------------------------------------------------------------
# The published views expose confidence and check level. The api role's grant set staying
# exactly {published_text: SELECT, published_verse: SELECT} is already asserted, independent
# of any hardcoded view list, by
# tests/test_grants_and_views.py::test_corpus_api_grant_set_is_exactly_select_on_published_views
# -- this migration adds no GRANT at all, so that test needs no change and is not repeated here.
# ----------------------------------------------------------------------------------------


def test_published_verse_exposes_confidence_and_check_level(owner_engine, api_engine, clean_corpus):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        _mark_check(conn, ids[0], "no-defect-found", [])
        promote(conn, text_id="conf", to_state="approved", author="Vipin Kaushik",
                confidence="certain")
    with api_engine.connect() as conn:
        row = conn.execute(sa.text(
            "SELECT confidence, check_level FROM published_verse WHERE verse_id = :v"),
            {"v": ids[0]}).mappings().one()
    assert row["confidence"] == "certain"
    assert row["check_level"] == "no-defect-found"


def test_published_verse_confidence_and_check_level_are_null_when_unapproved(
    owner_engine, api_engine, clean_corpus
):
    with owner_engine.begin() as conn:
        ids = _seed_translations(conn)
        _mark_check(conn, ids[0], "fails", ["wrong-script"])
        # Deliberately never promoted.
    with api_engine.connect() as conn:
        row = conn.execute(sa.text(
            "SELECT confidence, check_level FROM published_verse WHERE verse_id = :v"),
            {"v": ids[0]}).mappings().one()
    assert row["confidence"] is None
    assert row["check_level"] is None
