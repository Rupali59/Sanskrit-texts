"""No editorial English prose inside a Devanagari `text` field.

WHY THIS EXISTS. Three non-Sanskrit strings were sitting inside verses and were served as the
Sanskrit: an editor's gloss on the pluti vowel in `kena` 4.4 (``Extra `A'kAr is used in the sense
of comparison``), the same class in `taittiriya` 18.1, and the *edition's credit line* --
"By Dr. Sachchidanand Pathak, U.P. Sanskrit Sansthan, Lucknow, India." -- glued to the front of
`atharvaveda_samhita` 20.93.9. Removed 2026-09-30.

WHY THIS IS NOT A LATIN SWEEP, AND MUST NEVER BECOME ONE. A corpus-wide "remove Latin from
Devanagari" rule is 99.2% false positives -- it would destroy `samaveda_samhita`'s 1,866 arcika
reference suffixes and `brihat_samhita`'s 875 `(K...)` variant markers (G70) to fix 23 verses. So
this test does NOT assert "no Latin". It asserts that the survivors are exactly the ones below,
each of which is legitimate for a DIFFERENT reason, and fails when a new one appears.

THE THREE CLASSES THAT STAY, and why each is not a defect:
  * `brahmasphuta_siddhanta` x5 -- genuine OCR garbage (`QASSNSNN`, `paren fms it sy`). Needs a
    clean source or a re-OCR. A regex cannot tell it from the Devanagari around it.
  * `kena` 2.1, `kaivalya` 1.7/1.12 -- `var <reading>` is the sanskritdocuments edition's own
    variant apparatus; kena.html states the convention outright: "var indicates variations".
    Stripping the marker would silently promote an alternative reading into the main text, which
    is a worse corpus than a visible marker. Same class as G70.
  * `jataka_parijata` 2.49 -- `LOST PAGE`, a damage marker. The corpus records absent source
    rather than inventing it (see the Apastamba closure: 46 absent sutras recorded, never filled).

So a FAILURE here means one of: a new editorial gloss arrived, a listed verse was "cleaned" by a
sweep this file forbids, or a text was re-converted. Read the diff before changing the expectation.
"""

from __future__ import annotations

import json
import pathlib
import re

from sanskrit_texts.importer import corpus_files

ROOT = pathlib.Path(__file__).resolve().parent.parent
LATIN_RUN = re.compile(r"[A-Za-z]{3,}")

#: (text_id, chapter, shloka) -> why it is allowed. Anything not here is a finding.
#:
#: **This list is COUPLED to `tests/test_brahmasphuta_artifacts.py`** and the two must be edited
#: together. 2.28 was removed on 2026-09-30 when its page-header prefix (`QASSNSNN ( ३३ )`, the
#: next page's header leaking across a page break) was stripped. That edit was made in the other
#: file and this one caught it -- the "listed verse no longer carries Latin" assertion is what
#: makes the coupling visible instead of letting the two files drift into disagreeing.
ALLOWED = {
    ("brahmasphuta_siddhanta", "2", "10"): "OCR garbage",
    ("brahmasphuta_siddhanta", "14", "10"): "OCR garbage",
    ("brahmasphuta_siddhanta", "23", "5"): "OCR garbage",
    ("brahmasphuta_siddhanta", "24", "13"): "OCR garbage",
    ("kena_upanishad", "2", "1"): "var apparatus",
    ("kaivalya_upanishad", "1", "7"): "var apparatus",
    ("kaivalya_upanishad", "1", "12"): "var apparatus (mis-attached: belongs to v11)",
    ("jataka_parijata", "2", "49"): "LOST PAGE damage marker",
}

#: Strings that are never part of a verse, whatever text they appear in.
BANNED_SUBSTRINGS = (
    "U.P. Sanskrit Sansthan",          # an edition credit line
    "is used in the sense of",         # an editor's gloss
    "for prolonging the vowel",        # an editor's gloss
)


def _walk():
    for path in corpus_files(ROOT):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "chapters" not in doc:
            continue
        for ch in doc["chapters"]:
            for sh in ch.get("shlokas") or []:
                yield (str(doc.get("text_id")), str(ch.get("number")),
                       str(sh.get("number"))), (sh.get("text") or "")


def test_no_new_latin_in_devanagari():
    """The survivors are exactly ALLOWED -- no new ones, and none silently swept away."""
    found = {k for k, text in _walk() if LATIN_RUN.search(text)}

    # A derived population can go empty where a literal list cannot (rule:discernment-checks 2).
    walked = sum(1 for _ in _walk())
    assert walked > 50_000, f"only {walked} verses walked -- the scan has gone blind, not found nothing"

    new = found - set(ALLOWED)
    assert not new, (
        f"{len(new)} verse(s) carry Latin that this file does not account for: {sorted(new)}. "
        "Do NOT fix with a corpus-wide Latin sweep -- that is 99.2% false positives."
    )
    gone = set(ALLOWED) - found
    assert not gone, (
        f"{len(gone)} listed verse(s) no longer carry Latin: {sorted(gone)}. If a sweep removed "
        "apparatus or a damage marker, revert it; if a text was re-sourced, update ALLOWED."
    )


def test_banned_editorial_strings_are_absent_everywhere():
    """The three removed strings must not return, in any text."""
    hits = [
        (key, banned)
        for key, text in _walk()
        for banned in BANNED_SUBSTRINGS
        if banned in text
    ]
    assert not hits, f"editorial prose is back inside a verse: {hits}"
