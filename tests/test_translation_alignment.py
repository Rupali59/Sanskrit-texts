"""One translation must not be served for two different Sanskrit verses.

**The defect this exists for, measured 2026-09-24.** A translation run joined on the verse
NUMBER and dropped the chapter, so Sūtrasthāna's translations were written onto the
same-numbered verse of every other sthāna. **214 Aṣṭāṅga Hṛdaya verses were served a
translation belonging to a different verse** — ch2's `शुद्धे शुक्रार्तवे…` (conception) and
ch6's `जात-मात्रं विशोध्योल्बाद्…` (newborn care) both carried the Sūtrasthāna maṅgala verse.

**Nothing in this repo could see it**, which is why it needs its own test:

- `status` stayed `translated` and the served fields were non-empty, so the publication gate
  was satisfied.
- Counts were unchanged.
- **`(chapter, number)` keys stayed DISTINCT**, so `seed_texts.py`'s dedupe had nothing to
  catch — **G8's mirror image**: distinct keys over identical content multiply data as
  silently as duplicate keys delete it.
- No Devanāgarī appeared in the English, so no script check fired.
- 7,492 of 7,724 English strings were distinct — a distinctness ratio reads as healthy.

It was found by noticing the maṅgala verse appeared six times, i.e. by reading. **G31**: every
integrity check passes on wrong text, because they all check numbering.

**This is a RATCHET, not a pin.** `KNOWN` records what is already wrong; repairing an entry
makes the suite pass without anyone editing the expected set, and a newly-mistranslated text
fails. A test asserting the exact current total would have to be edited by whoever fixes the
data — which is how a check ends up loosened by the person it was meant to stop.

**Why this matters NOW:** `caraka_samhita` (9,654), `astanga_sangraha` (9,382) and
`susruta_samhita` (8,296) are still untranslated and carry the same repeating-verse-number
shape — 2,055, 2,088 and 1,686 numbers respectively that recur across chapters, up to 8 copies
each. If the join key is still wrong when the run reaches them, this test is what says so.
"""

from __future__ import annotations

import collections
import json
import pathlib

from sanskrit_texts.importer import corpus_files

REPO = pathlib.Path(__file__).resolve().parent.parent

#: text_id -> English strings each serving >1 distinct Sanskrit verse, as of 2026-09-24.
#: Every entry is a real defect awaiting repair, not an accepted state.
#: `astanga_hridaya`'s 32 are the residue of the join-key bug after its main repair.
KNOWN: dict[str, int] = {
    "astanga_hridaya": 32,
    "jataka_parijata": 8,
    "brihadaranyaka_upanishad": 8,
    "bhrigu_sutram": 3,
    "narada_smriti": 2,
    "jataka_tattva": 2,
    "chandogya_upanishad": 2,
    "brihat_samhita": 1,
}


def _misaligned(doc: dict) -> int:
    """English strings in `doc` served for more than one DISTINCT Sanskrit verse.

    Identical Sanskrit legitimately repeats — a genuinely repeated verse shares its
    translation, and that is not a defect. The defect is one translation over two different
    verses, so the comparison is over the set of `text` values, never over verse count.
    """
    by_english: dict[str, set[str]] = collections.defaultdict(set)
    for chapter in doc.get("chapters") or []:
        for shloka in chapter.get("shlokas") or []:
            english = (shloka.get("english") or "").strip()
            if english:
                by_english[english].add((shloka.get("text") or "").strip())
    return sum(1 for sanskrit in by_english.values() if len(sanskrit) > 1)


def _scan() -> dict[str, int]:
    found: dict[str, int] = {}
    for path in corpus_files(REPO):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(doc, dict) or "chapters" not in doc or "text_id" not in doc:
            continue
        n = _misaligned(doc)
        if n:
            found[doc["text_id"]] = n
    return found


def test_the_defect_is_detected() -> None:
    """Two different verses, one translation — the Aṣṭāṅga Hṛdaya shape, in miniature."""
    shared = "Salutations to that Supreme Physician."
    doc = {"text_id": "fixture", "chapters": [
        {"number": 1, "shlokas": [{"number": "1.1", "text": "क ख ग", "english": shared}]},
        {"number": 2, "shlokas": [{"number": "1.1", "text": "घ ङ च", "english": shared}]},
    ]}
    assert _misaligned(doc) == 1


def test_a_genuinely_repeated_verse_is_NOT_flagged() -> None:
    """The control. A verse that really does repeat shares its translation legitimately —
    flagging that would cry wolf on every text with a refrain."""
    doc = {"text_id": "fixture", "chapters": [
        {"number": 1, "shlokas": [{"number": 1, "text": "क ख ग", "english": "Same verse."}]},
        {"number": 2, "shlokas": [{"number": 1, "text": "क ख ग", "english": "Same verse."}]},
    ]}
    assert _misaligned(doc) == 0


def test_distinct_keys_do_not_hide_it() -> None:
    """G8's mirror image, pinned: the seeder dedupes on `(chapter, number)`, and the bug
    leaves those keys DISTINCT. A key-based check cannot see this and must not be trusted to."""
    doc = {"text_id": "fixture", "chapters": [
        {"number": n, "shlokas": [{"number": "1.1", "text": f"verse {n}", "english": "One rendering."}]}
        for n in (1, 2, 3)
    ]}
    keys = [(c["number"], s["number"]) for c in doc["chapters"] for s in c["shlokas"]]
    assert len(keys) == len(set(keys)), "fixture must have distinct keys, as the real defect did"
    assert _misaligned(doc) == 1, "the defect hid behind distinct keys"


def test_no_NEW_misaligned_translation_in_the_live_corpus() -> None:
    """The ratchet. Repairing a known text passes; a newly-mistranslated one fails."""
    found = _scan()

    # Control: if the walker found nothing, every assertion below is vacuous.
    assert sum(1 for _ in corpus_files(REPO)) > 50, "walker found almost nothing"

    new = {t: n for t, n in found.items() if t not in KNOWN}
    assert not new, (
        f"NEW misaligned translation(s): {new}. One English string is being served for two "
        f"different Sanskrit verses. The 2026-09-24 cause was a translation join keyed on the "
        f"verse NUMBER with the chapter dropped — `caraka_samhita`, `astanga_sangraha` and "
        f"`susruta_samhita` all carry repeating verse numbers and are the likely victims. "
        f"See this module's docstring."
    )

    worse = {t: (KNOWN[t], n) for t, n in found.items() if t in KNOWN and n > KNOWN[t]}
    assert not worse, f"misalignment GREW (known, now): {worse}"
