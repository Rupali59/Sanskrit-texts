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


#: A verse whose `text` is a bare division marker and nothing else. 24 characters is
#: comfortably above the longest real colophon seen here (`इति चतुर्थः प्रपाठकः`, 20) and far
#: below any actual verse.
BARE_COLOPHON_MAX = 24


def colophon_only_chapters(doc: dict[str, Any]) -> list[ColophonChapter]:
    """Every verse in `doc` that is a bare colophon standing where a verse should be.

    **Widened 2026-09-23, and the first version would have missed a real instance.** It looked
    only at one-verse chapters, because that is the shape `tejobindu_upanishad` and
    `kaushitaki_upanishad` present. `kaivalya_upanishad` presents the other one: the boundary
    was drawn at the colophon, the colophon landed at the HEAD of the next chunk, and that
    chunk then accumulated three more verses -- so the chapter has four verses and the bug is
    invisible to a one-verse rule. It was found by reading the text, not by the check, which
    is the whole argument for widening rather than adding a second rule beside it.

    So the rule is now about the VERSE, not the chapter: a `text` that is nothing but a
    division marker is never a verse, wherever it sits. A colophon at the END of a real verse
    is correct and is not flagged -- that is what a well-formed chapter looks like.

    **Filter on `ordinal_is_lower` for the certain ones, and the widening is why that matters.**
    Broadening from chapters to verses immediately produced a false positive:
    `apastamba_dharma_sutra` 2.5.11 is `इति हि ब्राह्मणम्` — *"for thus says the Brāhmaṇa"*,
    Āpastamba's citation formula and a genuine sūtra, sitting between 5.10 and 5.12 in a
    496-verse chapter. It matches the tail pattern because `ब्राह्मणम्` is also a division noun.

    **The ordinal separates them cleanly, and nothing else does.** A colophon says WHICH
    division it closes (`प्रथमः खण्डः`); a citation formula names no number. All three real
    instances carry an ordinal lower than their own chapter; the false positive carries none.
    Position does not discriminate — `kaivalya_upanishad`'s colophon sits at the HEAD of its
    chapter and Āpastamba's sits in the middle of one.
    """
    out: list[ColophonChapter] = []
    for ch in doc.get("chapters") or []:
        for v in ch.get("shlokas") or []:
            body = (v.get("text") or "").strip()
            if not body or len(body) > BARE_COLOPHON_MAX:
                continue
            if not COLOPHON_TAIL.search(body):
                continue
            out.append(ColophonChapter(
                text_id=doc.get("text_id", "<unknown>"),
                chapter=ch.get("number"),
                verse=v.get("number"),
                colophon_ordinal=colophon_ordinal(body),
                text_only_colophon=True,
                excerpt=body,
            ))
    return out
