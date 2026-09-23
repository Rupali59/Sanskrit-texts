"""Texts deliberately kept OUT of the corpus database, and why.

THIS IS A DECISION, NOT A FILTER. It is a named constant imported by the importer, the
exporter and `tests/test_key_census.py` so that excluding a text is visible in one place and
cannot become an undocumented `if` inside a loop.

**EMPTY SINCE 2026-09-23, and empty is the goal state rather than a gap.** An exclusion is a
text sitting in the corpus tree that the store must refuse -- so it is a standing hazard, not a
resolution. The right end for every entry is that the text LEAVES the tree, at which point the
exclusion has nothing to name. That is what happened to all four; the module stays because
`test_key_census.py` asserts against it and because the next bad text will want it.

## The four that were here, and where they went

Found 2026-09-16 when `check_inventory.py` began failing with "70 texts, 66 registry rows".
All four arrived untracked, were in no inventory, and three contained no genuine digitised
text. Every file parsed, every count was self-consistent, and `validate_corpus.py` accepted
them -- only the registry reconciler objected, and only because the rows were missing. Full
evidence: GOTCHAS **G62**.

Rupali's call 2026-09-16 was to exclude and defer. Resolved 2026-09-23:

| text | disposition |
|---|---|
| `deva_keralam` | **Quarantined** to `.quarantine/DevaKeralam/`. Generator output -- 401 verses collapsing to 18 skeletons, 384 with an empty `text` field carrying mojibake OCR English. Source `ChandraKalaNadi` restored to REFUSED |
| `dharmasindhu` | **Quarantined** to `.quarantine/Dharmasindhu/`. Sanskrit incoherent (Hindi mixed with garbled Devanagari); English a topic label. Source `Dharmasindhu` restored to REFUSED; G40 blocks it further |
| `taittiriya_brahmana` | **Handed to Youvan** at `Tushar/texts/_incoming/vk-2026-09-23/`. Real accented Sanskrit, excluded on SCOPE -- Brahmana is Youvan's layer |
| `taittiriya_aranyaka` | **Handed to Youvan**, same staging directory. Real Sanskrit, same scope rule |

The quarantine is reachable by no walker: every one skips dot-prefixed path components, and
`tests/test_quarantine.py` proves it against a mutated guard rather than asserting the
constant is present (`rule:safety-flag-needs-a-test`).

## One correction worth keeping

This docstring used to say *"`scripts/check_inventory.py` deliberately does NOT read it: its
drift row for these four is the standing record that they are here and unresolved."*

**That was half wrong, and the wrong half mattered.** `check_inventory.py:115` has always
imported `EXCLUDED_TEXTS` -- for the corpus-vs-DATABASE comparison, where an excluded text is
an *expected* absence. What it does not consult it for is the corpus-vs-REGISTRY comparison,
and that is the one the sentence was really about.

The distinction stopped being academic on 2026-09-16, when commit `ce5e8c0` added all four to
`docs/INVENTORY.md` as `HELD` / 100% / "real accented Sanskrit". That silenced the registry
drift row -- the very thing this docstring called the standing record -- and left the registry
asserting the opposite of this file about the same four texts, with every check green. A
record that one edit elsewhere can switch off was never a record.

If a text is ever excluded again: **keep it out of `INVENTORY.md`**, and let the registry
mismatch be the thing that keeps saying so.
"""

from __future__ import annotations

# text_id -> why it is excluded. Keep the reason with the id; a bare list rots into folklore.
# Empty by design -- see the module docstring. `test_key_census.py` fails if an entry here
# names a text that is no longer on disk, so a stale exclusion cannot survive quietly.
EXCLUDED_TEXTS: dict[str, str] = {}


def is_excluded(text_id: str) -> bool:
    """True when this text_id must not enter the database."""
    return text_id in EXCLUDED_TEXTS
