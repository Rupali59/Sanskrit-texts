"""`translation_status` — does a field hold a translation, or something wearing one's clothes?

Every fixture here is a shape this corpus actually produced. The module exists because
`status` is a claim and the served fields are the fact, and because eight distinct ways of
being "translated" without a translation all passed every other check in the repo.
"""

from __future__ import annotations

import json
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from sanskrit_texts.translation_status import (  # noqa: E402
    DECLARED_STATUSES,
    LABEL_REPEAT_MIN,
    check_file,
    check_text,
    check_value,
)

REPO = pathlib.Path(__file__).resolve().parent.parent
SA1 = "रागादि-रोगान् सततानुषक्तान् अ-शेष-काय-प्रसृतान् ।"
SA2 = "आयुः-कामयमानेन धर्मार्थ-सुख-साधनम् ।"
SA3 = "ब्रह्मा स्मृत्वायुषो वेदं प्रजापतिम् अजिग्रहत् ।"


def _verse(number, text, **kw):
    v = {"number": number, "text": text, "english": "", "hindi": "", "status": "untranslated"}
    v.update(kw)
    return v


def _doc(*verses, text_id="fixture", chapter=1):
    return {"text_id": text_id, "chapters": [{"number": chapter, "shlokas": list(verses)}]}


def test_a_clean_verse_is_translated_with_no_defects() -> None:
    st = check_text(_doc(_verse(1, SA1, english="Salutations to the Supreme Physician.",
                                hindi="सर्वश्रेष्ठ वैद्य को नमस्कार।", status="translated")))
    assert st.count("translated") == 1
    assert st.verses[0].defects == frozenset()
    assert st.verses[0].agrees


def test_the_sanskrit_echo_draft_is_not_a_translation() -> None:
    """60,524 verses. The field holds a label then the verse verbatim."""
    st = check_text(_doc(_verse(1, SA1, status="drafted",
                                english_draft=f"Classical text translation of X: {SA1}")))
    v = st.verses[0]
    assert v.effective == "untranslated", "an echo draft was counted as translated"
    assert "draft:en:template-prefix" in v.defects
    assert not v.is_corrupt, "a corrupt DRAFT is work-to-do, not a corrupt served translation"


def test_a_hindi_field_holding_the_sanskrit_does_not_make_a_verse_translated() -> None:
    """The false positive that nearly went out as a finding.

    42 Astanga Hridaya verses carry a PERFECT English translation beside a `hindi` field that is
    the Sanskrit verbatim. Reported without a language prefix this reads as a corrupt ENGLISH
    translation and sends a reviewer to the wrong field, so defects are language-prefixed.
    """
    st = check_text(_doc(_verse(1, SA1, status="translated",
                                english="If the patient cannot afford those, bind the body at night.",
                                hindi=SA1)))
    v = st.verses[0]
    assert v.effective == "partial", "Sanskrit in `hindi` was accepted as a Hindi translation"
    assert "hi:sanskrit-echo" in v.defects
    assert "en:sanskrit-echo" not in v.defects, "the defect was blamed on the wrong field"
    assert not any(d.startswith("en:") for d in v.defects), "the English is clean and must read so"


def test_one_translation_serving_two_different_verses_is_flagged() -> None:
    """214 Astanga Hridaya verses. The join dropped the sthana and keyed on the verse number.

    `(chapter, number)` keys stay DISTINCT, so the seeder dedupe has nothing to catch (G8's
    mirror image) and every count stays correct.
    """
    shared = "Salutations to that Supreme Physician who destroyed all diseases."
    st = check_text(_doc(_verse("1.1", SA1, english=shared, hindi="क", status="translated"),
                         _verse("1.2", SA2, english=shared, hindi="ख", status="translated")))
    assert all("en:misaligned" in v.defects for v in st.verses)
    assert st.count("translated") == 0, "a misaligned translation was counted as translated"
    assert st.corrupt == 2


def test_identical_translations_over_IDENTICAL_sanskrit_are_NOT_flagged() -> None:
    """The control. A genuinely repeated verse legitimately repeats its translation."""
    st = check_text(_doc(_verse("1.1", SA1, english="Same verse.", hindi="क", status="translated"),
                         _verse("2.1", SA1, english="Same verse.", hindi="क", status="translated")))
    assert not any("en:misaligned" in v.defects for v in st.verses)
    assert st.count("translated") == 2


def test_a_refrain_whose_copies_differ_only_in_punctuation_is_neither_label_nor_misaligned() -> None:
    """`caraka_samhita`'s closing formula ends each adhyaya as `…भगवानात्रेयः //` in one place and
    `…भगवानात्रेयः//` in another -- the same verse. Compared raw, `check_text` read the copies as
    different verses, so the shared (correct) translation became `misaligned`, and at three copies
    `label-only`. Switching to `normalise_sanskrit` took the backlog's BAD column 539 -> 375 on
    2026-10-02 (Caraka 114 -> 89, Suśruta 152 -> 84, Atharvaveda 73 -> 2). Literal fixture."""
    formula = "इति ह स्माह भगवानात्रेयः"
    copies = [f"{formula} //", f"{formula}//", f"{formula} ॥", f" {formula}//"]
    st = check_text(_doc(*[_verse(f"{i}.2", sa, english="Thus said the venerable Lord Atreya.",
                                  hindi="ऐसा भगवान आत्रेय ने कहा।", status="translated")
                           for i, sa in enumerate(copies, 1)]))
    assert not any(v.defects & {"en:misaligned", "en:label-only"} for v in st.verses), (
        [sorted(v.defects) for v in st.verses])
    assert st.count("translated") == len(copies)


def test_one_english_over_three_genuinely_different_verses_is_still_flagged() -> None:
    """The other side of the refrain test: normalising must not hide the block-summary defect
    (`astanga_sangraha` 7.54/7.56 -- one sentence served over different ingredient lists)."""
    summary = "The light and nourishing substances are to be consumed, especially for the weak."
    st = check_text(_doc(*[_verse(f"7.{n}", sa, english=summary, hindi="हल्के पदार्थ।",
                                  status="translated")
                           for n, sa in ((54, "तृट्च्छर्दिश्रमनुन्मन्थः शीतः"),
                                         (55, "विष्टम्भि मूत्रलं हृद्यं"),
                                         (56, "यथाद्रव्यगुणं च सर्वम्"))]))
    assert all({"en:misaligned", "en:label-only"} <= v.defects for v in st.verses)


def test_a_repeated_label_is_detected_and_a_short_real_translation_is_not() -> None:
    """Length cannot separate these; repetition can.

    A minimum-word floor classified 85 genuine `jaimini_sutra` drafts as boilerplate --
    "Jupiter in the 4th gives a wooden house." is a complete translation of a terse sutra.
    """
    label = "Scholarly English translation of this chapter, following Kulluka Bhatta."
    verses = [_verse(i, f"क{i}", english_draft=label, status="drafted")
              for i in range(LABEL_REPEAT_MIN)]
    verses.append(_verse(99, "ख", english_draft="Jupiter in the 4th gives a wooden house.",
                         status="drafted"))
    st = check_text(_doc(*verses))
    assert sum(1 for v in st.verses if "draft:en:label-only" in v.defects) == LABEL_REPEAT_MIN
    assert "draft:en:label-only" not in st.verses[-1].defects, (
        "a short but genuine translation was condemned as boilerplate"
    )


def test_an_undeclared_status_is_reported() -> None:
    """`draft_promoted` reached 19 `garga_hora` verses and nothing rejected it."""
    st = check_text(_doc(_verse(1, SA1, english="A.", hindi="क", status="draft_promoted")))
    assert "undeclared-status" in st.verses[0].defects
    assert "draft_promoted" not in DECLARED_STATUSES


def test_a_served_field_beside_an_unconsumed_draft_is_reported() -> None:
    """Promotion is defined as clearing the draft it consumed; 869 verses are in neither state."""
    st = check_text(_doc(_verse(1, SA1, english="A real translation.", hindi="क",
                                english_draft="A different rendering.", status="translated")))
    assert "draft-not-cleared" in st.verses[0].defects


def test_latin_inside_the_sanskrit_field_is_reported() -> None:
    """Uncleaned OCR: `निरोगं दीर्घजीवितं aed |`. It corrupts the SOURCE, not the translation."""
    st = check_text(_doc(_verse(1, "लग्नाधिपतिर्लग्ने निरोगं दीर्घजीवितं aed |",
                                english="If the lord of the ascendant is in the ascendant.",
                                hindi="क", status="translated")))
    v = st.verses[0]
    assert "latin-in-source" in v.defects
    assert v.effective == "translated", "a source defect must not mark the TRANSLATION untranslated"


def test_status_disagreement_is_visible() -> None:
    st = check_text(_doc(_verse(1, SA1, english="A.", hindi="क", status="untranslated")))
    assert st.verses[0].effective == "translated"
    assert not st.verses[0].agrees
    assert st.disagreements == 1


def test_wrong_script_both_ways() -> None:
    assert "wrong-script" in check_value("en", "कखग", SA1)
    assert "wrong-script" in check_value("hi", "abc", SA1)
    assert "wrong-script" not in check_value("en", "abc", SA1)


def test_short_sanskrit_hindi_gloss_containing_the_term_is_not_an_echo() -> None:
    """Regression for `quiet-juggling-cherny` Lane D. Below `SANSKRIT_ECHO_MIN_LEN`,
    `stripped[:40]` used to be the WHOLE Sanskrit, so a correct Hindi gloss quoting a short
    term was condemned as an echo. Live example: `bhrigu_sutram` ch3 v37."""
    dev = "मायावादी"
    hindi = "वह मायावादी (भ्रम में विश्वास रखने वाला या छल करने वाला) होगा।"
    assert "sanskrit-echo" not in check_value("hi", hindi, dev)


def test_long_sanskrit_genuinely_echoed_into_hindi_still_fails() -> None:
    """The fix is scoped to short Sanskrit only -- the real defect class (`astanga_hridaya`)
    must keep firing."""
    dev = "श्री गणेशाय नमः तस्मात् सर्वप्रयत्नेन " * 3  # > 40 characters
    value = "हिन्दी में: " + dev[:40] + " आगे"
    assert "sanskrit-echo" in check_value("hi", value, dev)


# Live values as LITERALS (2026-10-02), not loaded from the corpus: once the corpus is repaired
# they stop existing there, and a test that reads them would silently start checking nothing.
# `jataka_parijata` 12.44 -- a hyphen and the danda spacing differ inside the first 40
# characters, so neither exact equality nor the raw prefix test saw it.
_REPUNCTUATED_DEV = "विक्रमेशगुरू लग्नं गतौ गोभीतिसूचकौ ।\nराहुणा वा फणिक्रान्तराशिपेन युतौ यदि ॥"
_REPUNCTUATED_HI = "विक्रमेश-गुरू लग्नं गतौ गोभीतिसूचकौ। राहुणा वा फणिक्रान्तराशिपेन युतौ यदि।"
# `astanga_sangraha` 44.7 -- the same names, comma-separated, THEN Hindi of its own. A real
# translation. A skeleton-PREFIX rule flags it; that is why the rule is whole-value equality.
_NAME_LIST_DEV = "पाण्डुरा रक्तपदिका भृङ्गा पिङ्गा त्रिमण्डला । पूतिर्वीराण्डजाःसप्त सौम्या लूताः"
_NAME_LIST_HI = "पाण्डुरा, रक्तपदिका, भृङ्गा, पिङ्गा, त्रिमण्डला, पूति और वीराण्डजा—ये सात सौम्या लूताएँ हैं।"


@pytest.mark.parametrize("checker", ["translation_status", "checks"])
def test_hindi_that_only_repunctuates_the_sanskrit_is_an_echo(checker: str) -> None:
    """172 of Suśruta's served Hindi values were the verse with `/` turned into `;` or `।`;
    the backlog reported the text complete. Both checkers must see it."""
    assert _REPUNCTUATED_DEV.strip() != _REPUNCTUATED_HI, "fixture must not be an exact echo"
    assert _REPUNCTUATED_DEV[:40] not in _REPUNCTUATED_HI, "fixture must defeat the prefix rule"
    if checker == "checks":
        from sanskrit_texts.checks import check_translation
        found = set(check_translation("hi", _REPUNCTUATED_HI, _REPUNCTUATED_DEV)[1])
    else:
        found = check_value("hi", _REPUNCTUATED_HI, _REPUNCTUATED_DEV)
    assert "sanskrit-echo" in found


@pytest.mark.parametrize("checker", ["translation_status", "checks"])
def test_a_hindi_name_list_that_adds_its_own_words_is_not_an_echo(checker: str) -> None:
    if checker == "checks":
        from sanskrit_texts.checks import check_translation
        found = set(check_translation("hi", _NAME_LIST_HI, _NAME_LIST_DEV)[1])
    else:
        found = check_value("hi", _NAME_LIST_HI, _NAME_LIST_DEV)
    assert "sanskrit-echo" not in found


def test_check_file_refuses_a_non_corpus_document() -> None:
    """Absence must be attributable (rule:discernment-checks §2) -- never a silent clean result."""
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump({"not": "a corpus doc"}, fh)
        p = fh.name
    with pytest.raises(ValueError, match="not a corpus document"):
        check_file(p)


def test_the_rules_agree_with_the_canonical_checker_on_the_live_corpus() -> None:
    """`sanskrit_texts.checks.check_translation` is canonical for template-prefix /
    sanskrit-echo / wrong-script. This module restates them so `scripts/` can import it under
    bare `python3`; **a restatement nothing compares is a fork.**"""
    from sanskrit_texts.checks import check_translation
    from sanskrit_texts.importer import corpus_files

    shared = {"template-prefix", "sanskrit-echo", "wrong-script"}
    checked = disagreements = 0
    for p in corpus_files(REPO):
        doc = json.loads(p.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "chapters" not in doc:
            continue
        for ch in doc["chapters"]:
            for s in ch.get("shlokas") or []:
                sanskrit = (s.get("text") or "").strip()
                for lang, field in (("en", "english"), ("hi", "hindi"),
                                    ("en", "english_draft"), ("hi", "hindi_draft")):
                    value = (s.get(field) or "").strip()
                    if not value:
                        continue
                    checked += 1
                    mine = check_value(lang, value, sanskrit) & shared
                    theirs = set(check_translation(lang, value, sanskrit)[1]) & shared
                    if mine != theirs:
                        disagreements += 1
    assert checked > 10000, "too few values examined for this to mean anything"
    assert disagreements == 0, (
        f"{disagreements} of {checked} values judged differently from checks.check_translation"
    )
