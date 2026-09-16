"""Texts deliberately kept OUT of the corpus database, and why.

THIS IS A DECISION, NOT A FILTER. It is a named constant imported by the importer and by
`tests/test_key_census.py` so that excluding a text is visible in one place and cannot become
an undocumented `if` inside a loop. `scripts/check_inventory.py` deliberately does NOT read it:
its drift row for these four is the standing record that they are here and unresolved.

Found 2026-09-16 when `check_inventory.py` began failing with "70 texts, 66 registry rows".
All four are untracked, were never in any inventory, and three contain no genuine digitised
text at all -- every file parses, every count is self-consistent, and `validate_corpus.py`
accepts them, which is why only the registry reconciler objected. Full evidence: GOTCHAS G62.

Rupali's call, 2026-09-16: ignore them for now; the database is built without them.
Resolution (delete / quarantine / hand to Youvan) is tracked in the workspace TODOS.md.
"""

from __future__ import annotations

# text_id -> why it is excluded. Keep the reason with the id; a bare list rots into folklore.
EXCLUDED_TEXTS: dict[str, str] = {
    "deva_keralam": (
        "FABRICATED. 300 verses collapse to 2 skeletons -- every verse is the template "
        "'देवकेरलम् (चन्द्रकलानिडी) <rashi> लग्ने नाड्यंश <N>: सूर्यादिग्रहाणाम् शुभदुष्टफलम् ॥' "
        "with only the rasi and a counter 1..300 varying. Its source, ChandraKalaNadi, is a "
        "REFUSED acquisition row."
    ),
    "dharmasindhu": (
        "RAW OCR, not text. 500 verses of which 54 contain '=== page N ===' page markers. "
        "Also a REFUSED acquisition row, and G40 records this text as blocked on a mula/tika "
        "classifier that has already failed once -- so this is a premature attempt at it."
    ),
    "taittiriya_aranyaka": (
        "WRONG TEXT. 250 verses carry 8 distinct bodies repeated ~32x each, and the bodies are "
        "Rigveda 1.1.1 ('अग्निमीळे पुरोहितं') and Shukla Yajurveda 1.1 ('इषे त्वोर्जे त्वा') "
        "wrapped in a 'प्रपाठक N अनुवाक M:' citation template. Aranyaka is also Youvan's scope."
    ),
    "taittiriya_brahmana": (
        "WRONG REPO, and not even the same content. Its Devanagari is genuine (properly "
        "accented), but Brahmana is Youvan's scope and 0 of its 400 verses overlap Youvan's "
        "legitimate 1,832-verse copy at Tushar/texts/Brahmana/KrishnaYajurveda/."
    ),
}


def is_excluded(text_id: str) -> bool:
    """True when this text_id must not enter the database."""
    return text_id in EXCLUDED_TEXTS
