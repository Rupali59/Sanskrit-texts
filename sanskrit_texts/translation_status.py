"""What a verse's translation state ACTUALLY is, as against what `status` claims.

`status` is a cached claim; the served `english`/`hindi` fields are the fact, and the Mongo
seeder reads the fields (**G50**). This module derives the fact, and treats a field holding
something that is not a translation as *not translated* rather than as translated.

**Every defect below was found in this corpus, and every one passed all existing checks**
(**G31**: the integrity checks all check numbering, and numbering stays self-consistent):

  template-prefix   `Classical text translation of <Title>: ` then the verse verbatim. 60,524
                    verses. Distinct-skeleton ratio rates these 0.95-1.00, "looks real" --
                    they vary because the EMBEDDED SANSKRIT varies (**G55**).
  sanskrit-echo     en: >30% of the value is Devanagari / hi: the value IS the Sanskrit.
  wrong-script      en: no Latin at all / hi: no Devanagari at all.
  stub-heading      `Chapter 21, Shloka 11 - Description of ...` -- a topic label.
  label-only        English that DESCRIBES a translation instead of being one, detected by
                    repetition within the text: "Scholarly English translation of Chapter 4,
                    Shloka 1, following Kulluka Bhatta and Medhatithi." **Length cannot detect
                    these** -- a floor misclassified 85 genuine `jaimini_sutra` drafts, of which
                    "Jupiter in the 4th gives a wooden house." is a complete translation of a
                    terse sutra. Repetition can.
  misaligned        This verse's served translation is byte-identical to another verse's while
                    the two Sanskrit texts DIFFER. 214 Astanga Hridaya verses were served
                    Sutrasthana's translations because the join dropped the sthana and keyed on
                    the verse number alone -- and `(chapter, number)` keys stayed distinct, so
                    the seeder dedupe had nothing to catch (**G8**'s mirror image).
  draft-not-cleared A served field AND an unconsumed `*_draft`. Promotion is defined as
                    clearing the draft it consumed; 869 verses are in neither state, and 545 of
                    those hold a DIFFERENT text in the draft, so nothing records which was
                    verified.
  undeclared-status A `status` outside the four the schema declares. `draft_promoted` appeared
                    on 19 `garga_hora` verses and no check rejected it -- `status` is a plain
                    string, exactly like `category` (**G51**).
  latin-in-source   Latin letters inside the SANSKRIT field: `निरोगं दीर्घजीवितं aed |`.
                    Uncleaned OCR. It corrupts the source, not the translation, but it is
                    reported here because it is what a translator will be handed.
  not-nfc           Normalisation regression. `4195d69` NFC-normalised the whole corpus.

**`sanskrit_texts.checks.check_translation` remains canonical for the first three**, and this
module is deliberately stdlib-only so `scripts/` can import it under bare `python3` -- `checks`
imports SQLAlchemy, which is why a mirror of its rules existed in `translation_backlog.py` at
all. `tests/test_translation_status.py` asserts the two agree on every verse in the live corpus,
so this is a single definition rather than a second one.
"""

from __future__ import annotations

import collections
import dataclasses
import json
import pathlib
import re
import unicodedata
from typing import Any, Iterable

#: The four the schema declares. `CLAUDE.md` §"Field notes"; nothing enforces it, which is why
#: `draft_promoted` reached 19 verses unnoticed.
DECLARED_STATUSES = frozenset({"translated", "partial", "untranslated", "drafted"})

#: Mirrors `checks.check_translation`. Pinned to it by test, never edited independently.
TEMPLATE_PREFIX = re.compile(r"^Classical text translation of [^:]+: ")
SANSKRIT_ECHO_SHARE = 0.30

#: Mirrors `checks._SANSKRIT_ECHO_MIN_LEN`. Below this, `stripped[:40]` is the WHOLE Sanskrit,
#: not a prefix of it, so the hi containment check degenerates into "mentions the term at all" --
#: a correct gloss quoting a short term (`मायावादी`) or a shared placeholder (`..........`) both
#: match. Exact equality has no such degenerate case and stays unconditional.
SANSKRIT_ECHO_MIN_LEN = 40

#: `[0-9]`, never `\d` -- **G17**: Python's `\d` matches Devanagari digits.
STUB_HEADING = re.compile(r"^Chapter [0-9]+,? Shloka [0-9]+ *[-–:]")

LATIN = re.compile(r"[A-Za-z]")
LATIN_WORD = re.compile(r"[A-Za-z']{2,}")
DEVANAGARI_RUN = re.compile(r"[ऀ-ॿ।॥]+")

#: A normalised English body served over this many DISTINCT verses in ONE text is boilerplate. 3 rather
#: than 2 so a pair of genuinely similar short renderings is not condemned.
LABEL_REPEAT_MIN = 3

_FAIL_CODES = ("template-prefix", "sanskrit-echo", "wrong-script", "stub-heading",
               "label-only", "misaligned")
FAILS = frozenset(f"{lang}:{code}" for lang in ("en", "hi") for code in _FAIL_CODES)
"""Defects meaning the field does not hold a translation. The rest are warnings: real
translation is present but its bookkeeping is wrong."""


def _devanagari_share(value: str) -> float:
    chars = [c for c in value if not c.isspace()]
    if not chars:
        return 0.0
    return sum(1 for c in chars if "ऀ" <= c <= "ॿ") / len(chars)


def _english_body(value: str, sanskrit: str) -> str:
    """The English left once the verse's own source text is removed.

    Keyed on the `text` FIELD rather than on script, and that is load-bearing: the one live
    verse this rescues is `atharvaveda_samhita`'s, whose Sanskrit field has a bibliographic
    credit leaked into it (`By Dr. Sachchidanand Pathak, U.P. Sanskrit Sansthan, Lucknow`).
    Left in, that English reads as verse-specific. Whatever the source field holds is not a
    translation of itself.
    """
    body = value.replace(sanskrit, " ") if sanskrit and sanskrit in value else value
    return DEVANAGARI_RUN.sub(" ", body)


def _normalised_body(value: str, sanskrit: str) -> str:
    return re.sub(r"[0-9]+", "N", " ".join(LATIN_WORD.findall(_english_body(value, sanskrit))).lower())


def normalise_sanskrit(text: str) -> str:
    """Whitespace and division markers only -- never letters.

    MOVED HERE 2026-10-02 from `tests/test_translation_alignment.py`, which now imports it. Until
    then `check_text` compared RAW Sanskrit for `misaligned`/`label-only`, so the two instruments
    disagreed about what "a different verse" is, and 393 refrain pairs this function correctly
    folds read as defects. One definition, two callers.

    The comparison is over DISTINCT Sanskrit, so two renderings of the SAME verse must collapse
    to one string or the check reports a defect that is not there. Measured 2026-09-25:
    `caraka_samhita` served 7 groups, of which 4 were the closing formula
    `इति ह स्माह भगवानात्रेयः` differing ONLY by a space before `//` -- six verses of identical
    Sanskrit counted as six different verses.

    Deliberately conservative: it touches whitespace, daṇḍas, pipes and slashes and nothing else,
    so it cannot merge two genuinely different verses. Verified across the whole corpus the day it
    was added -- `caraka_samhita` fell 7 -> 3 and **every other text was unchanged**, which is the
    property that makes it safe rather than merely convenient.

    WIDENED 2026-09-30, to three more classes, each measured before it was added. The first
    version's "never letters" rule was the right instinct and slightly too narrow: it left three
    ways for ONE verse to look like two, all of them found in the Vedic Saṃhitās, none of them a
    difference in the text itself.

      citation numerals   `४ १ जितमस्माकम…` vs `५ २ जितमस्माकम…` -- atharvaveda 16.8. The leading
                          digits are the ārcika/aṣṭaka reference, a CITATION COMPONENT, not the
                          mantra. Both ASCII and Devanāgarī digits, spelled out as ranges: `\\d`
                          is Unicode-aware and would be right here by accident and wrong
                          elsewhere (**G17**).
      avagraha            `स्वऽरस्माकं` vs `स्वरस्माकं` -- the elided-a mark, present in one
                          rendering of a verse and absent in another. This is the one that bends
                          "never letters", and it is admitted rather than hidden: `ऽ` marks an
                          elision, so dropping it cannot merge two verses that differ in any
                          sounded syllable.
      space at a sandhi   `अस्मिन्भरे` vs `अस्मिन् भरे` -- rigveda 3.38.10 / 3.39.9, two copies of
      juncture            the refrain `शुनं हुवेम मघवानमिन्द्रम्…` that closes 14 hymns. Collapsing
                          runs of whitespace was never enough; the difference is a space that
                          exists in one and not the other, so the whitespace goes entirely.

    THE FILE ALREADY WARNED AGAINST THE VERSION I WROTE FIRST, and I did not read it. The
    `samaveda_samhita` note in `KNOWN` above says, in as many words, *"NOT fixable by widening
    `_normalise` to strip numerals: those are citation components, and stripping them would merge
    any two verses differing only by a number"*. That is exactly what the unanchored strip did, and
    `test_distinct_keys_do_not_hide_it` caught it -- its fixture is three verses differing only by
    a digit, and they collapsed to one, so a real misalignment became invisible to the check built
    to find it. Anchoring to the LEADING run is what makes the two consistent: a citation reference
    is a prefix, a sine table's numbers are not. `samaveda`'s entry stays at 1 and stays correct.

    MEASURED CORPUS-WIDE BEFORE THE CHANGE, which is the only reason to believe it:
    `atharvaveda_samhita` **4 -> 1**, `samaveda_samhita` **1 -> 0**, and **all nine other texts
    reporting groups were unchanged** -- narada_smriti, bhrigu_sutram, jataka_tattva,
    jataka_parijata, brihat_samhita, chandogya_upanishad, brihadaranyaka_upanishad,
    caraka_samhita, susruta_samhita. Total 37 -> 33. The four it removes are the four verified by
    hand as the same mantra twice; the one it LEAVES in atharvaveda is a real defect (4.12.8, a
    ritual header sitting in a shloka row). A widening that had merged a genuine pair would have
    shown up as some other text falling, and none did.
    """
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[।॥|/]+", " ", text)
    # LEADING numerals only. Stripping digits everywhere was the first attempt and it is wrong:
    # `test_distinct_keys_do_not_hide_it` builds three verses differing ONLY by a digit and asserts
    # the defect is still seen, and digit-stripping made all three identical -- a real misalignment
    # rendered invisible by the check meant to find it. The corpus has the same shape for real:
    # `surya_siddhanta` carries sine tables (`...1171, 1345, 1528...`) whose verses differ only in
    # their numbers. A citation reference is a PREFIX, so anchor it and the hazard goes away.
    text = re.sub(r"^[\s0-9०-९]+", "", text)
    text = text.replace("ऽ", "")                 # avagraha
    return re.sub(r"\s+", "", text)                   # incl. a space at a sandhi juncture


def _letter_skeleton(s: str) -> str:
    """Mirrors `checks._letter_skeleton` -- Devanagari letters only, NFC; no whitespace,
    punctuation, danda or digit. Whole-value equality only; the reason is on the canonical copy."""
    s = unicodedata.normalize("NFC", s)
    return "".join(c for c in s if "ऀ" <= c <= "ॣ" or "॰" <= c <= "ॿ")


def check_value(lang: str, value: str, sanskrit: str) -> set[str]:
    """Defects visible in ONE translation value. `lang` is "en" or "hi".

    Cross-verse defects (`label-only`, `misaligned`) need the whole text and are added by
    `check_text`; this function cannot see them and does not pretend to.
    """
    found: set[str] = set()
    if not value.strip():
        return found
    if TEMPLATE_PREFIX.match(value):
        found.add("template-prefix")
    if STUB_HEADING.match(value):
        found.add("stub-heading")
    if lang == "en":
        if _devanagari_share(value) > SANSKRIT_ECHO_SHARE:
            found.add("sanskrit-echo")
        if not LATIN.search(value):
            found.add("wrong-script")
    else:
        stripped = sanskrit.strip()
        if stripped and (
            value.strip() == stripped
            or (len(stripped) >= SANSKRIT_ECHO_MIN_LEN and stripped[:SANSKRIT_ECHO_MIN_LEN] in value)
            or (_letter_skeleton(stripped) and _letter_skeleton(value) == _letter_skeleton(stripped))
        ):
            found.add("sanskrit-echo")
        if not any("ऀ" <= c <= "ॿ" for c in value):
            found.add("wrong-script")
    if unicodedata.normalize("NFC", value) != value:
        found.add("not-nfc")
    return found


@dataclasses.dataclass(frozen=True)
class VerseStatus:
    """One verse's real state. `effective` ignores `status` entirely and reads the fields."""

    chapter: Any
    number: Any
    declared: str | None
    effective: str
    defects: frozenset[str]

    #: `drafted` is a claim about the DRAFT field; both it and `untranslated` assert that
    #: nothing is served, so they are the same claim about the served fields. Treating them as
    #: different reported 60,475 "disagreements" that were simply the whole draft backlog.
    _EQUIVALENT = {"drafted": "untranslated"}

    @property
    def agrees(self) -> bool:
        """Whether `status` matches what the served fields actually hold."""
        declared = self._EQUIVALENT.get(self.declared, self.declared)
        return declared == self.effective

    @property
    def is_corrupt(self) -> bool:
        """Corruption of the SERVED text only. `draft:`-prefixed defects are excluded by
        construction -- they describe work not yet done, not a bad translation on the shelf."""
        return bool(self.defects & FAILS)

    @property
    def draft_defects(self) -> frozenset[str]:
        return frozenset(d.split(":", 1)[1] for d in self.defects if d.startswith("draft:"))

    def __str__(self) -> str:
        bits = f"{self.chapter}.{self.number} {self.effective}"
        if not self.agrees:
            bits += f" (status says {self.declared!r})"
        if self.defects:
            bits += " [" + ", ".join(sorted(self.defects)) + "]"
        return bits


@dataclasses.dataclass(frozen=True)
class TextStatus:
    """A whole file's translation state, corruption counted as untranslated."""

    text_id: str
    verses: tuple[VerseStatus, ...]
    defects: collections.Counter

    @property
    def total(self) -> int:
        return len(self.verses)

    def count(self, effective: str) -> int:
        return sum(1 for v in self.verses if v.effective == effective)

    @property
    def corrupt(self) -> int:
        return sum(1 for v in self.verses if v.is_corrupt)

    @property
    def disagreements(self) -> int:
        return sum(1 for v in self.verses if not v.agrees)

    @property
    def percent_translated(self) -> float:
        return 100.0 * self.count("translated") / self.total if self.total else 0.0

    def summary(self) -> str:
        parts = [f"{self.text_id}: {self.total:,} verses",
                 f"{self.count('translated'):,} translated "
                 f"({self.percent_translated:.0f}%)",
                 f"{self.count('partial'):,} partial",
                 f"{self.count('untranslated'):,} untranslated"]
        if self.corrupt:
            parts.append(f"**{self.corrupt:,} corrupt**")
        if self.disagreements:
            parts.append(f"{self.disagreements:,} disagree with `status`")
        line = " · ".join(parts)
        if self.defects:
            line += "\n  defects: " + ", ".join(
                f"{k} {v:,}" for k, v in sorted(self.defects.items(), key=lambda x: -x[1]))
        return line


def _iter_shlokas(doc: dict[str, Any]) -> Iterable[tuple[Any, dict[str, Any]]]:
    for chapter in doc.get("chapters") or []:
        for shloka in chapter.get("shlokas") or []:
            yield chapter.get("number"), shloka


def check_text(doc: dict[str, Any]) -> TextStatus:
    """Every verse in one corpus document, with corruption counted as NOT translated.

    Two passes, because two defects are only visible across the whole text:
    `label-only` (the same English body repeated) and `misaligned` (one translation serving
    two different Sanskrit verses).
    """
    rows = list(_iter_shlokas(doc))

    # body -> the DISTINCT verses (by `normalise_sanskrit`) it is served for. A refrain repeats
    # identical Sanskrit and legitimately shares one translation; a label is pasted over many
    # different verses. Counting verses instead of distinct verses condemned every refrain.
    bodies: dict[str, set[str]] = collections.defaultdict(set)
    by_english: dict[str, set[str]] = collections.defaultdict(set)
    for _chapter, s in rows:
        sanskrit = (s.get("text") or "").strip()
        for field in ("english", "english_draft"):
            value = (s.get(field) or "").strip()
            if value:
                bodies[_normalised_body(value, sanskrit)].add(normalise_sanskrit(sanskrit))
        served = (s.get("english") or "").strip()
        if served:
            by_english[served].add(normalise_sanskrit(sanskrit))

    verses: list[VerseStatus] = []
    tally: collections.Counter = collections.Counter()
    for chapter, s in rows:
        sanskrit = (s.get("text") or "").strip()
        english = (s.get("english") or "").strip()
        hindi = (s.get("hindi") or "").strip()

        # Language-prefixed, because an unlabelled `sanskrit-echo` is unattributable: measured
        # on this corpus, 42 Astanga Hridaya verses carry a PERFECT English translation beside a
        # `hindi` field holding the Sanskrit verbatim. Reported bare, that reads as a corrupt
        # English translation and sends a reviewer to the wrong field.
        defects = {f"en:{c}" for c in check_value("en", english, sanskrit)}
        defects |= {f"hi:{c}" for c in check_value("hi", hindi, sanskrit)}

        # Draft defects are reported under a `draft:` prefix and never fold into `effective`.
        # A corrupt DRAFT is not a corrupt translation -- it means the work is still to do, and
        # conflating the two is what made 60,524 echo drafts read as "awaiting review".
        for lang, field in (("en", "english_draft"), ("hi", "hindi_draft")):
            value = (s.get(field) or "").strip()
            for code in check_value(lang, value, sanskrit):
                defects.add(f"draft:{lang}:{code}")

        # Attribute the label to the field that actually carries it. A boilerplate DRAFT means
        # the verse is untranslated; a boilerplate SERVED value means something unreal is being
        # published, which is a different and worse fact.
        if english and len(bodies[_normalised_body(english, sanskrit)]) >= LABEL_REPEAT_MIN:
            defects.add("en:label-only")
        draft_en = (s.get("english_draft") or "").strip()
        if draft_en and len(bodies[_normalised_body(draft_en, sanskrit)]) >= LABEL_REPEAT_MIN:
            defects.add("draft:en:label-only")

        if english and len(by_english.get(english, ())) > 1:
            defects.add("en:misaligned")

        if s.get("status") not in DECLARED_STATUSES:
            defects.add("undeclared-status")
        for served, draft in (("english", "english_draft"), ("hindi", "hindi_draft")):
            if (s.get(served) or "").strip() and (s.get(draft) or "").strip():
                defects.add("draft-not-cleared")
        # A Latin WORD, never a single letter: `a`/`b`/`c` pada markers are legitimate notation
        # in this corpus's references (`0504a` in Samaveda's arcika citations). Requiring one
        # letter flagged 2,777 verses of which 1,866 were every verse of `samaveda_samhita`
        # and 869 of `brihat_samhita` -- a detector that fires on whole healthy texts is noise.
        if LATIN_WORD.search(sanskrit):
            defects.add("latin-in-source")

        # `effective` reads the SERVED fields only, and counts a corrupt one as not translated.
        served_defects = {d for d in defects if not d.startswith("draft:")}
        good_en = bool(english) and not ({f"en:{c}" for c in check_value("en", english, sanskrit)} & FAILS) \
            and not (served_defects & {"en:label-only", "en:misaligned"})
        good_hi = bool(hindi) and not ({f"hi:{c}" for c in check_value("hi", hindi, sanskrit)} & FAILS)

        if good_en and good_hi:
            effective = "translated"
        elif good_en or good_hi:
            effective = "partial"
        else:
            effective = "untranslated"

        verses.append(VerseStatus(chapter, s.get("number"), s.get("status"),
                                  effective, frozenset(defects)))
        tally.update(defects)

    return TextStatus(doc.get("text_id", "<unknown>"), tuple(verses), tally)


def check_file(path: str | pathlib.Path) -> TextStatus:
    """`check_text` for a corpus JSON file on disk.

    Raises rather than returning an empty result when the file cannot be read: absence must be
    attributable (`rule:discernment-checks` §2), and a silent zero here would read as a clean
    text.
    """
    path = pathlib.Path(path)
    doc = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(doc, dict) or "chapters" not in doc:
        raise ValueError(f"{path} is not a corpus document (no `chapters`)")
    return check_text(doc)


def main(argv: list[str] | None = None) -> int:
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="+", type=pathlib.Path)
    ap.add_argument("--verses", action="store_true", help="list every defective verse")
    args = ap.parse_args(argv)
    worst = 0
    for f in args.files:
        try:
            status = check_file(f)
        except (OSError, ValueError, json.JSONDecodeError) as e:
            print(f"could not check {f}: {type(e).__name__}: {e}")
            worst = max(worst, 2)
            continue
        print(status.summary())
        if args.verses:
            for v in status.verses:
                if v.defects or not v.agrees:
                    print(f"    {v}")
        if status.corrupt:
            worst = max(worst, 1)
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
