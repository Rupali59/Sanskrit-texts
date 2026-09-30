"""A verse whose source text is a LACUNA must never carry a translation.

WHY THIS EXISTS. `minaraja_yavana_jataka` had 19 verses whose `text` is Pingree's lacuna notation
-- a run of dots marking text absent from every manuscript -- and all 19 carried `english` and
`hindi` with `status: "translated"`. Five of those were substantive, confident, domain-correct
prose invented for verses that do not exist:

    20.63  "Budha with Mangala: Produces a person fond of quarrels, attached to unrighteous..."
    22.49  "Shukra endowed with the strength of Surya's path (Ayanabala) makes a person very..."
     9.5   "Surya in Mesha aspected by Shukra: (Inferred) Brings wealth, enjoyment..."

9.5 labelled itself `(Inferred)`. They sat in the SERVED fields, so `seed_texts.py` would have
published them to the public `/texts` API -- against the workspace hard rule that no machine-written
interpretation reaches a public surface. Removed 2026-09-30.

WHY NOTHING ELSE CAUGHT IT, which is the part worth keeping. These read as excellent translations:
fluent, correctly formatted, using the right technical vocabulary. Every machine check passed them.
`tests/test_translation_alignment.py` compares a translation to its Sanskrit and cannot fire when
there IS no Sanskrit; the confidence checker that quarantined 76 served non-translations (`f3f7c6c`)
scores the text and these score well. **Fluency is what made them invisible** -- the same signal
`rule:enforcement-watches-itself` names. The only instrument that sees it is the source: the
critical edition has 17 whole-verse lacunae of the form `॥ ६२॥ .......... ॥ ६३॥`, so there is
nothing to translate and never was.

THE RULE THIS ENFORCES IS THE CORPUS'S OWN. Absent source is RECORDED, never invented -- the same
discipline as the Apastamba closure ("46 sutras are ABSENT from the OCR and were recorded, never
invented"), `jataka_parijata` 2.49's `LOST PAGE`, and G62. A lacuna verse is `untranslated` with
empty translation fields; the dots in `text` are the record.
"""

from __future__ import annotations

import json
import pathlib
import re

from sanskrit_texts.importer import corpus_files

ROOT = pathlib.Path(__file__).resolve().parent.parent

#: A verse body that is only lacuna dots, optionally with its verse-number marker.
LACUNA = re.compile(r"^[.\s]*(॥[\s०-९\d]*॥)?[.\s]*$")


def _lacuna_verses():
    for path in corpus_files(ROOT):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "chapters" not in doc:
            continue
        for ch in doc["chapters"]:
            for sh in ch.get("shlokas") or []:
                text = (sh.get("text") or "").strip()
                if text and LACUNA.match(text):
                    yield (str(doc.get("text_id")), str(ch.get("number")),
                           str(sh.get("number"))), sh


def test_a_lacuna_verse_carries_no_translation():
    """The load-bearing assertion: no source text means no translation, served OR draft."""
    found = list(_lacuna_verses())

    # Derived populations can silently go empty (rule:derive-dont-curate). 19 known in minaraja.
    assert len(found) >= 15, (
        f"only {len(found)} lacuna verses matched -- the pattern has gone blind, it has not "
        "found that they were all repaired"
    )

    offenders = {
        key: {f: sh[f][:80] for f in ("english", "hindi", "english_draft", "hindi_draft") if sh.get(f)}
        for key, sh in found
        if any(sh.get(f) for f in ("english", "hindi", "english_draft", "hindi_draft"))
    }
    assert not offenders, (
        f"{len(offenders)} verse(s) whose source is a lacuna carry a translation: {offenders}. "
        "There is no Sanskrit at these verses in the critical edition, so any translation was "
        "invented. Record the absence; never fill it."
    )


def test_a_lacuna_verse_is_marked_untranslated():
    """`status` must agree. All 19 read `translated` while translating nothing."""
    wrong = {key: sh.get("status") for key, sh in _lacuna_verses()
             if sh.get("status") != "untranslated"}
    assert not wrong, (
        f"lacuna verses with a status other than 'untranslated': {wrong}. A verse with no source "
        "text cannot be 'translated' or 'partial'."
    )
