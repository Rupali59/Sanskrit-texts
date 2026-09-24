"""The ECHO/DRAFT split: is a draft a translation, or the Sanskrit wearing a label?

Split out 2026-09-23. Before it, `translation_backlog.py` reported every populated
`english_draft` as `VERIFY-DRAFT` -- "written, awaiting review". 67,965 of 69,037 contained no
English at all, so the stated backlog understated the real work by roughly sixty-fold.

**Two instruments were tried first and both were wrong. Each has a test here so that
"simplifying" the classifier fails loudly rather than silently restoring the old number.**

  * `test_echo_drafts_are_distinct_but_not_translations` -- a distinct-skeleton ratio rated the
    echoes 0.95-1.00, "looks real". They vary because the EMBEDDED SANSKRIT varies. G55.
  * `test_a_short_real_translation_is_NOT_an_echo` -- a minimum-word floor then misclassified 85
    genuine `jaimini_sutra` drafts. Length does not separate them; repetition does.
"""

from __future__ import annotations

import json
import pathlib
import subprocess
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from translation_backlog import (  # noqa: E402
    STUB_RE,
    TEMPLATE_MIN,
    classify_drafts,
    draft_body,
    skeleton,
)

REPO = pathlib.Path(__file__).resolve().parent.parent

SA = "रागादि-रोगान् सततानुषक्तान् अ-शेष-काय-प्रसृतान् अ-शेषान् ।"
SA2 = "आयुः-कामयमानेन धर्मार्थ-सुख-साधनम् ।"
SA3 = "ब्रह्मा स्मृत्वायुषो वेदं प्रजापतिम् अजिग्रहत् ।"


def test_the_echo_shape_is_detected() -> None:
    """`astanga_hridaya`'s actual shape: a label, then the verse verbatim."""
    items = [(f"Classical text translation of Astanga Hridaya: {s}", s)
             for s in (SA, SA2, SA3)]
    english, echo = classify_drafts(items)
    assert (english, echo) == (0, 3), "the Sanskrit-echo drafts were counted as translations"


def test_echo_drafts_are_distinct_but_not_translations() -> None:
    """The instrument that failed first: they ARE all distinct strings.

    A distinct-skeleton ratio over the RAW drafts returns 1.00 here and calls them real.
    The distinctness comes from the Sanskrit, which is exactly what `draft_body` removes.
    """
    drafts = [f"Classical text translation of Astanga Hridaya: {s}" for s in (SA, SA2, SA3)]
    assert len(set(drafts)) == 3, "fixture is wrong -- these must be distinct strings"
    assert len({skeleton(b) for b in (draft_body(d, s) for d, s in zip(drafts, (SA, SA2, SA3)))}) == 1, (
        "once the Sanskrit is stripped the three drafts must collapse to ONE skeleton"
    )


def test_a_short_real_translation_is_NOT_an_echo() -> None:
    """The second failed instrument, pinned.

    These are verbatim `jaimini_sutra` drafts. A minimum-English-word floor classified all of
    them as echoes; they are complete translations of terse sutras.
    """
    items = [
        ("Jupiter in the 4th gives a wooden house.", "गुरौ दारुगृहम्"),
        ("Ketu causes restriction or impediment.", "केतौ रोधः"),
        ("Venus gives devotion to Goddess Lakshmi.", "शुक्रे लक्ष्मीभक्तिः"),
    ]
    english, echo = classify_drafts(items)
    assert (english, echo) == (3, 0), "short but genuine translations were discarded as echoes"


def test_repetition_not_length_is_the_discriminator() -> None:
    """A LONG label repeated is an echo; a SHORT unique rendering is not."""
    long_label = ("Scholarly English translation of this chapter and verse, "
                  "following Kulluka Bhatta and Medhatithi throughout.")
    items = [(long_label, "क")] * TEMPLATE_MIN + [("Mars gives valour.", "ख")]
    english, echo = classify_drafts(items)
    assert echo == TEMPLATE_MIN, "a repeated label escaped because it was long"
    assert english == 1, "a short unique translation was swept up with it"


def test_the_template_threshold_has_both_sides() -> None:
    """Below the threshold a repeat is tolerated; at it, condemned. Both directions asserted."""
    below = [("A repeated rendering.", "क")] * (TEMPLATE_MIN - 1)
    assert classify_drafts(below) == (TEMPLATE_MIN - 1, 0), "tolerated repeats were condemned"
    at = [("A repeated rendering.", "क")] * TEMPLATE_MIN
    assert classify_drafts(at) == (0, TEMPLATE_MIN), "boilerplate at the threshold slipped through"


def test_draft_body_removes_whatever_the_SOURCE_field_holds_not_merely_devanagari() -> None:
    """`draft_body` earns its place on exactly one live verse, and the case is not Devanagari.

    `skeleton()` already keeps only Latin words, so stripping Devanagari changes almost nothing
    -- measured 2026-09-23, removing `draft_body` entirely moved **1 verse of 69,037**. That one
    is `atharvaveda_samhita`, whose SANSKRIT field has a bibliographic credit leaked into it:

        By Dr. Sachchidanand Pathak, U.P. Sanskrit Sansthan, Lucknow, India. अभि प्र गोपतिं...

    The draft repeats it after the usual label. Left in, that English is verse-specific enough
    to read as a translation. The rule that saves it is not "strip Devanagari" but **"whatever
    the verse's own source field holds is not a translation of it"** -- so the removal is keyed
    on the `text` field, not on script. Do not narrow it back to a Devanagari filter.
    """
    credit = "By Dr. Sachchidanand Pathak, U.P. Sanskrit Sansthan, Lucknow, India. अभि प्र गोपतिम्"
    items = [(f"Classical text translation of Atharvaveda Samhita (Shaunaka): {credit}", credit),
             (f"Classical text translation of Atharvaveda Samhita (Shaunaka): {SA}", SA),
             (f"Classical text translation of Atharvaveda Samhita (Shaunaka): {SA2}", SA2)]
    english, echo = classify_drafts(items)
    assert (english, echo) == (0, 3), (
        "a credit line leaked into the Sanskrit field was counted as a translation"
    )


def test_a_draft_that_is_bare_sanskrit_is_an_echo() -> None:
    """No label at all -- just the verse. There is no English to verify."""
    assert classify_drafts([(SA, SA)]) == (0, 1)
    assert classify_drafts([(SA, "")]) == (0, 1), "unmatched Sanskrit must still be stripped"


def test_stub_pattern_does_not_match_devanagari_digits() -> None:
    """G17: Python's `\\d` matches Devanagari digits, so this pattern uses `[0-9]`."""
    assert STUB_RE.match("Chapter 21, Shloka 11 - Description of the effects")
    assert not STUB_RE.match("Chapter २१, Shloka ११ - Description of the effects"), (
        "`\\d` has crept back in -- it matches Devanagari digits"
    )


def test_every_live_draft_is_classified_exactly_once() -> None:
    """The conservation law. A verse must not vanish between the two columns."""
    from translation_backlog import scan
    rows, parsed = scan()
    assert parsed > 50, "the walker found almost nothing -- assertions below would be vacuous"

    counted = sum(r["draft_en"] + r["draft_echo"] for r in rows)
    actual = 0
    for p in sorted(REPO.rglob("*.json")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in ("docs", ".git") or rel.parts[0].startswith("."):
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not j.get("text_id"):
            continue
        actual += sum(1 for ch in j.get("chapters") or []
                      for s in ch.get("shlokas") or []
                      if (s.get("english_draft") or "").strip())
    assert counted == actual, f"{actual} drafts on disk, {counted} classified"


def test_the_mirrored_rules_agree_with_the_canonical_checker() -> None:
    """The mirror guard. `sanskrit_texts.checks.check_translation` is canonical.

    `translation_backlog.py` cannot import it -- that module pulls SQLAlchemy and the script is
    documented as runnable under bare `python3` -- so three of its rules are restated there.
    **A restatement nothing compares is a fork**, and this repo has paid for that shape
    repeatedly. This test runs in the venv, where BOTH are importable, and asserts they agree
    on every draft in the live corpus.

    If this fails, do not edit the expectation: make the two agree.
    """
    from sanskrit_texts.checks import check_translation
    from translation_backlog import fails_canonical_checks

    checked = disagreements = 0
    for p in sorted(REPO.rglob("*.json")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in ("docs", ".git") or rel.parts[0].startswith("."):
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if not j.get("text_id"):
            continue
        for ch in j.get("chapters") or []:
            for s in ch.get("shlokas") or []:
                draft = (s.get("english_draft") or "").strip()
                if not draft:
                    continue
                checked += 1
                canonical = check_translation("en", draft, (s.get("text") or "").strip())[0]
                if (canonical == "fails") != fails_canonical_checks(draft):
                    disagreements += 1

    assert checked > 1000, "almost no drafts examined -- this assertion would be vacuous"
    assert disagreements == 0, (
        f"{disagreements} of {checked} drafts are judged differently by "
        f"translation_backlog.fails_canonical_checks and checks.check_translation. "
        f"The mirror has drifted from the canonical checker."
    )


def test_the_script_runs_and_reports_both_columns() -> None:
    r = subprocess.run([sys.executable, "scripts/translation_backlog.py"],
                       cwd=REPO, capture_output=True, text=True, timeout=300)
    assert r.returncode == 0, f"exit {r.returncode}\n{r.stdout}\n{r.stderr}"
    assert "ECHO" in r.stdout and "DRAFT" in r.stdout
    assert "VERIFY-DRAFT" in r.stdout
    assert "are NOT translations" in r.stdout, (
        "the summary no longer says echoes are not translations -- that sentence is the "
        "whole point of the split"
    )


def test_could_not_run_is_distinguishable_from_a_clean_backlog(tmp_path, monkeypatch) -> None:
    """rule:discernment-checks §2 -- absence must be attributable."""
    import translation_backlog as tb
    monkeypatch.setattr(tb, "REPO", tmp_path)
    assert tb.main() == 2, "an empty tree reported a clean backlog instead of 'could not run'"
