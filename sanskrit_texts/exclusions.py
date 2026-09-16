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
    # REASONS RE-MEASURED 2026-09-16 ~15:00. All four files were rewritten at 14:11-14:12, so
    # the first version of these reasons -- and GOTCHAS G62's table -- described a state that
    # no longer exists. They are UNTRACKED, so git cannot tell you they moved; re-derive before
    # trusting any count here.
    "deva_keralam": (
        "384 of 401 verses have an EMPTY `text` field while carrying English, and that English "
        "is raw OCR with mojibake: 'I, Venkatesa, belonging to Kasyapa Gotra, 3 2arsferfaara "
        "affeer Wet: | res'. A translation with no source text cannot be verified against "
        "anything. (Was 300 verses collapsing to 2 template skeletons before the rewrite.) "
        "Its source, ChandraKalaNadi, is a REFUSED acquisition row."
    ),
    "dharmasindhu": (
        "89 verses whose Sanskrit is incoherent -- 'जो समुद्र उसके शुष्ककारकः लक्षमरूप "
        "रुकिमिणीको वुद्धिके चोरः' mixes Hindi with garbled Devanagari -- and whose English is "
        "a topic label rather than a translation. (Was 500 verses of raw OCR carrying "
        "'=== page N ===' markers.) A REFUSED acquisition row, and G40 records this text as "
        "blocked on a mula/tika classifier that has already failed once."
    ),
    "taittiriya_aranyaka": (
        "The SANSKRIT IS NOW REAL -- 'भद्रं कर्णेभिः शृणुयाम देवाः' then the Aruna Prashna, "
        "415 verses, all distinct. (It was Rigveda 1.1.1 wrapped in a Taittiriya citation "
        "template.) Still excluded on TWO grounds that the rewrite did not touch: the English "
        "is a topic label ('Taittiriya Aranyaka (P1.2) - Aruna Prashna (Solar Mantras): Mantra "
        "text an...'), and Aranyaka is YOUVAN'S SCOPE, not this repo's."
    ),
    "taittiriya_brahmana": (
        "1,687 verses of genuine accented Sanskrit, English genuine on some verses and a topic "
        "label on others. (Was 400 verses.) Excluded on SCOPE regardless of quality: Brahmana "
        "belongs to Youvan, whose tree already holds a 1,832-verse copy at "
        "Tushar/texts/Brahmana/KrishnaYajurveda/. Two copies of one text in two repos is the "
        "problem, not the content."
    ),
}


def is_excluded(text_id: str) -> bool:
    """True when this text_id must not enter the database."""
    return text_id in EXCLUDED_TEXTS
