"""SC-001's detector: a one-verse chapter whose verse ends in a colophon.

The bug is a converter drawing a chapter boundary AT the colophon instead of after it, so the
verse carrying that colophon is pushed into the next chapter and becomes a pseudo-chapter.
Filed 2026-09-07 against `tejobindu_upanishad`; two live instances found here 2026-09-23.

Nothing caught it for sixteen days because every check in this repo checks NUMBERING, and
numbering is exactly what stays self-consistent when a verse is re-parented rather than lost.
That is G31's lesson in a new place.

**The live-corpus test below is a RATCHET, not a pin.** It asserts no colophon-only chapter
exists outside the known set — so repairing one makes it pass, and a newly-converted text
arriving broken makes it fail. A test asserting the exact current count would have to be
edited by the person fixing the data, which is how a check ends up being loosened by whoever
it was meant to stop.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from sanskrit_texts.importer import corpus_files
from sanskrit_texts.structure_checks import (
    COLOPHON_TAIL,
    colophon_only_chapters,
    colophon_ordinal,
)

REPO = pathlib.Path(__file__).resolve().parent.parent

# EMPTY as of 2026-09-23: both live instances were repaired, so the ratchet now guards a clean
# corpus. That is the shape it was built for — a repair empties it without anyone editing the
# expected set, and the next text converted wrong re-fills it.
KNOWN: set[str] = set()

# The ratchet keys on the CERTAIN hits only -- those whose colophon names a division number
# lower than the chapter holding it. Widening the detector from chapters to verses immediately
# turned up `apastamba_dharma_sutra` 2.5.11, `इति हि ब्राह्मणम्` ("for thus says the Brāhmaṇa"),
# which is a real sūtra between 5.10 and 5.12 and matches only because `ब्राह्मणम्` is also a
# division noun. It names no ordinal; all three real instances do. That is the discriminator.


def _chapter(number, verses):
    return {"number": number, "title": "", "shlokas": verses}


def _verse(number, text):
    return {"number": number, "text": text, "english": "", "hindi": "",
            "status": "untranslated"}


def _doc(text_id, chapters):
    return {"text_id": text_id, "title_sa": "प", "title_en": "F", "category": "fixture",
            "chapters": chapters}


def test_the_defect_is_detected() -> None:
    doc = _doc("fixture_text", [
        _chapter(1, [_verse(1, "क ख ग"), _verse(2, "घ ङ च")]),
        _chapter(2, [_verse(1, "प्रथमोऽध्यायः")]),      # closes chapter ONE, sits in TWO
        _chapter(3, [_verse(1, "छ ज झ"), _verse(2, "ञ ट ठ")]),
    ])
    found = colophon_only_chapters(doc)
    assert len(found) == 1, f"expected 1, got {found}"
    assert found[0].chapter == 2
    assert found[0].colophon_ordinal == 1
    assert found[0].ordinal_is_lower, "the decisive tell was not derived"


def test_a_healthy_text_is_NOT_flagged() -> None:
    """The control. A detector that fires on everything is as useless as one that never does."""
    doc = _doc("healthy", [
        _chapter(1, [_verse(1, "क ख ग"), _verse(2, "घ ङ च ॥ इति प्रथमोऽध्यायः")]),
        _chapter(2, [_verse(1, "छ ज झ")]),
    ])
    assert colophon_only_chapters(doc) == [], (
        "a colophon at the END of a multi-verse chapter is CORRECT — that is what the "
        "converter should produce, and flagging it would cry wolf on every well-formed text"
    )


def test_a_one_verse_chapter_without_a_colophon_is_NOT_flagged() -> None:
    doc = _doc("short_chapter", [
        _chapter(1, [_verse(1, "क ख ग")]),
        _chapter(2, [_verse(1, "घ ङ च")]),
    ])
    assert colophon_only_chapters(doc) == []


def test_iti_alone_does_not_make_a_colophon() -> None:
    """`इति` means "thus" and is ubiquitous in Sanskrit prose.

    An unanchored test for it flagged 8 verses of which 6 were ordinary text (measured
    2026-09-23) — including four in taittiriya_upanishad ending `तदप्येष श्लोको भवति`.
    The pattern is anchored to the TAIL and to a division noun for exactly that reason.
    """
    assert not COLOPHON_TAIL.search("इति होवाच तदप्येष श्लोको भवति")
    assert COLOPHON_TAIL.search("इति प्रथमोऽध्यायः")


@pytest.mark.parametrize("text,expected", [
    ("प्रथमोऽध्यायः", 1),
    ("द्वितीयः खण्डः", 2),
    ("इति तृतीयोऽध्यायः", 3),
    ("कश्चित् अध्यायः", None),  # a division noun with no ordinal
])
def test_ordinal_extraction(text: str, expected: int | None) -> None:
    assert colophon_ordinal(text) == expected


def test_no_NEW_colophon_chapter_in_the_live_corpus() -> None:
    """The ratchet. Repairing a known instance passes; a new one fails."""
    offenders = set()
    for path in corpus_files(REPO):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(doc, dict) or "chapters" not in doc or "text_id" not in doc:
            continue
        if [c for c in colophon_only_chapters(doc) if c.ordinal_is_lower]:
            offenders.add(doc["text_id"])

    # Control: if the walker found no texts at all, every assertion here is vacuous.
    assert sum(1 for _ in corpus_files(REPO)) > 50, "walker found almost nothing"

    new = offenders - KNOWN
    assert not new, (
        f"NEW colophon-only chapter(s) in {sorted(new)} — SC-001 has recurred. The converter "
        f"drew a chapter boundary AT a colophon instead of after it; see "
        f"scripts/sanskrit-convert/ISSUES.md SC-001."
    )


def test_a_citation_formula_is_not_mistaken_for_a_colophon() -> None:
    """The false positive the widening produced, pinned so a future widening cannot re-admit it.

    `इति हि ब्राह्मणम्` is Āpastamba's citation formula and a genuine sūtra. It matches the
    tail pattern (`ब्राह्मणम्` is a division noun) and must never be classed as certain,
    because it names no division number.
    """
    doc = _doc("apastamba_like", [
        _chapter(1, [_verse("5.10", "क ख ग")]),
        _chapter(2, [_verse("5.11", "इति हि ब्राह्मणम्"), _verse("5.12", "घ ङ च")]),
    ])
    found = colophon_only_chapters(doc)
    assert found, "the detector should still surface it for a human"
    assert not any(c.ordinal_is_lower for c in found), (
        "a citation formula naming no ordinal was classed CERTAIN — the ratchet would now "
        "fail on a text that is not broken"
    )
