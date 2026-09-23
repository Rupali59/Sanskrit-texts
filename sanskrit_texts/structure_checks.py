"""Structural defects a schema check cannot see, because the file is well-formed.

SC-001: a converter that splits chapters ON the colophon instead of AFTER it pushes the
verse carrying that colophon into the NEXT chapter, where it becomes a one-verse
pseudo-chapter. Filed 2026-09-07 against `tejobindu_upanishad` (9 chapters reported for a
6-chapter text) and found still live here 2026-09-23.

**Why nothing caught it.** Every verse parses, every chapter key is well-formed,
`validate_corpus.py` reports the file `ok`, and the shloka total is unchanged — the verse was
not lost, only re-parented. It is G31's lesson in a new place: the integrity checks all check
numbering, and numbering is exactly what stays self-consistent.

**The decisive tell is the ORDINAL, not the length.** A colophon names the division it CLOSES,
so `प्रथमोऽध्यायः` ("first chapter") sitting inside chapter 2 says the boundary was drawn one
unit early. A one-verse chapter is suspicious; a one-verse chapter whose colophon ordinal is
lower than its own chapter number is the defect.

**This module reports, it does not repair.** The two live instances are not repairable
mechanically — `kaushitaki_upanishad`'s stray record carries a real English translation
against a colophon Sanskrit, and `kaivalya_upanishad`'s chapter 2 is separately missing
verses 21 and 23. Guessing either would invent text, which is the most expensive mistake this
corpus has recorded (G31). Detection is mechanical; repair is a human reading an edition.
"""

from __future__ import annotations

import dataclasses
import re
from typing import Any

# A colophon CLOSES a division and sits at the very end of the verse. Anchored to the tail on
# purpose: `इति` alone means "thus" and is ubiquitous -- an unanchored test flagged 8 verses
# of which 6 were ordinary prose (measured 2026-09-23).
COLOPHON_TAIL = re.compile(
    r"(ऽध्यायः|अध्यायः|खण्डः|उपनिषत्|ब्राह्मणम्|प्रपाठकः|अनुवाकः|सर्गः|पटलः)\s*॥?\s*$"
)

# Devanagari ordinal stems, in the sandhi-stripped form a colophon uses.
ORDINALS = {
    "प्रथम": 1, "द्वितीय": 2, "तृतीय": 3, "चतुर्थ": 4, "पञ्चम": 5,
    "षष्ठ": 6, "सप्तम": 7, "अष्टम": 8, "नवम": 9, "दशम": 10,
    "एकादश": 11, "द्वादश": 12, "त्रयोदश": 13, "चतुर्दश": 14, "पञ्चदश": 15,
}


@dataclasses.dataclass(frozen=True)
class ColophonChapter:
    text_id: str
    chapter: Any
    verse: Any
    colophon_ordinal: int | None
    text_only_colophon: bool
    excerpt: str

    @property
    def ordinal_is_lower(self) -> bool:
        """The decisive tell: a colophon closing division N sitting inside chapter > N."""
        try:
            return self.colophon_ordinal is not None and self.colophon_ordinal < int(self.chapter)
        except (TypeError, ValueError):
            return False

    def __str__(self) -> str:
        bits = []
        if self.ordinal_is_lower:
            bits.append(f"closes division {self.colophon_ordinal}")
        if self.text_only_colophon:
            bits.append("no verse content")
        why = f" ({', '.join(bits)})" if bits else ""
        return f"{self.text_id} ch {self.chapter} verse {self.verse}{why}: {self.excerpt!r}"


def colophon_ordinal(text: str) -> int | None:
    """The division number a colophon names, or None when it does not name one."""
    for stem, n in ORDINALS.items():
        if stem in text:
            return n
    return None


def colophon_only_chapters(doc: dict[str, Any]) -> list[ColophonChapter]:
    """Every one-verse chapter in `doc` whose single verse ENDS in a colophon.

    Returns the SC-001 candidates. A caller wanting only the certain ones filters on
    `ordinal_is_lower`; the rest are worth a human glance but may be legitimate (a genuinely
    one-verse final division exists in some texts).
    """
    out: list[ColophonChapter] = []
    for ch in doc.get("chapters") or []:
        verses = ch.get("shlokas") or []
        if len(verses) != 1:
            continue
        v = verses[0]
        body = (v.get("text") or "").strip()
        if not COLOPHON_TAIL.search(body):
            continue
        ordinal = colophon_ordinal(body)
        # "Only a colophon" = the verse carries the marker and essentially nothing else. The
        # threshold is deliberately generous: tejobindu's orphan was a real half-verse PLUS a
        # colophon, and that is still the same defect -- this flag only tells the repairer
        # whether content would be lost by deleting the record.
        out.append(ColophonChapter(
            text_id=doc.get("text_id", "<unknown>"),
            chapter=ch.get("number"),
            verse=v.get("number"),
            colophon_ordinal=ordinal,
            text_only_colophon=len(body) <= 24,
            excerpt=body[-40:],
        ))
    return out
