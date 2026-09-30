"""`brahmasphuta_siddhanta` -- what was repaired, and what must stay untouched.

WHY THIS EXISTS. 75 verses were repaired on 2026-09-30 by stripping page furniture and stray
characters that leaked out of the OCR. Thirteen were deliberately NOT repaired. This pins both, so
that a later "clean up the Latin" pass cannot quietly take the thirteen with it, and so that a
regression in the converter cannot quietly put the seventy-five back.

**The corpus-wide sweep this file exists to prevent is 99.2% false positives.** `samaveda_samhita`
carries 1,866 arcika reference suffixes and `brihat_samhita` 875 `(K....)` variant markers (G70);
both are legitimate Latin-adjacent apparatus. The repair was scoped to this one text for that
reason, and the scoping is the finding, not an implementation detail.

WHAT MADE A REPAIR SAFE, since "it looked like noise" is not a reason. Each candidate was anchored
by its longest Devanagari run in the two RICHER OCR passes on disk (`native-devanagari/txt`,
`render-193/txt`) and kept only if the stripped text still appeared intact there. The pass the
corpus was built FROM (`ocr/txt`) proves nothing -- the stray character is in it by construction --
which is why the gate reads the other two.

THE ONE THAT PROVES THE GATE WORKS: verse 19.4 held `नुजले l गृहभित्यग्`. A lone `l` looks exactly
like noise. `render-193/txt` renders that same position `नुजले'।` -- it is a mis-OCR'd **danda**,
and stripping it would have deleted real punctuation. It was substituted, not removed, on the
evidence of our own scan rather than the licence-barred witness.
"""

from __future__ import annotations

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

from check_brahmasphuta import classify  # noqa: E402

from sanskrit_texts.importer import corpus_files  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parent.parent
TEXT_ID = "brahmasphuta_siddhanta"

#: The verses that still carry non-Devanagari, and why each is NOT a bug to be swept.
#: Every one needs the 336pp scan or a structural decision; none can be fixed by a regex.
KNOWN_UNREPAIRED = {
    # --- still corrupt, and our own scan cannot settle them -------------------------------
    "2.10": "glyph corruption -- garbled in ALL passes, so it is in the print",
    "2.53": "scanner artifact `[EE or ———`; render-193 does not cover this region",
    "15.52": "glyph corruption `इड ठाक तलचच Nh ५१`; render-193 does not cover this region",
    "24.13": "glyph corruption `nefe`; render-193 does not cover this region",
    "23.5": "render-193 HAS the verse but with different noise (`EE`) -- neither pass is clean",
    # CORRECTED 2026-09-30: these were recorded as "printed footnote marks" earlier the same day.
    # `€` is the OCR's reading of the NUMERAL ९ -- 10 of its 17 occurrences sit inside a verse
    # marker `॥ € ॥`, and `॥ ९ ॥` appears only twice in 336 pages against 20-28 for its
    # neighbours. See G71. So this is a lost verse marker, not decoration; stripping it destroys
    # structure. `©` appears twice, both inside a scanner-edge garbage run.
    # 5.10 became 5.9 when the merged verse was split on its own `॥ € ॥` (G71): the marker WAS
    # the boundary, so the stray `A` that preceded it now sits in the first of the two verses.
    "5.9": "stray `A`; its `€` was the lost ९ marker and is now the split point (G71)",
    "6.4": "`©` is scanner-edge noise (both occurrences sit in a garbage run)",
    "12.52": "stray `t` between Devanagari. render-193 does not cover it and native-devanagari "
             "carries the same `t`, so it is UNCONFIRMED. Probably a mis-OCR'd danda like 19.4's "
             "`l`, but our own scan cannot show it and the witness is licence-barred as a source.",
    # --- NOT corruption. MISLABELLING, which is a different defect and a different fix -----
    # G12: "a MISSING record may be a MISLABELLED one, and counts cannot tell you". Both of these
    # were on the recoverable list until the neighbours were read. The verse the corpus calls
    # 14.10 is verse NINE's body (14.9 is an apparent gap); the verse it calls 19.9 is the body
    # render-193 closes with ॥८॥ (19.8 is an apparent gap). Fixing them means RENUMBERING, which
    # moves citation targets -- so it is a decision, not a repair, and is deliberately not made.
    "14.10": "MISLABELLED: holds verse 9's body + the first word of verse 10. 14.9 reads absent",
    "19.9": "MISLABELLED: holds the body render-193 closes with ॥८॥. 19.8 reads absent",
}


def _verses():
    for path in corpus_files(ROOT):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or doc.get("text_id") != TEXT_ID:
            continue
        for ch in doc["chapters"]:
            for sh in ch.get("shlokas") or []:
                yield f"{ch['number']}.{sh['number']}", (sh.get("text") or "")
        return


def test_the_unrepaired_set_is_exactly_what_we_decided_to_leave():
    """No new artifact, and none of the thirteen silently swept away."""
    found = {key for key, text in _verses() if classify(text)}

    walked = sum(1 for _ in _verses())
    assert walked > 600, f"only {walked} verses walked -- the walker has gone blind, not found a clean text"

    new = found - set(KNOWN_UNREPAIRED)
    assert not new, (
        f"{len(new)} verse(s) carry non-Devanagari that nothing accounts for: {sorted(new)}. "
        "Do NOT fix with a corpus-wide Latin sweep."
    )
    swept = set(KNOWN_UNREPAIRED) - found
    assert not swept, (
        f"{len(swept)} verse(s) listed as unrepairable are now clean: {sorted(swept)}. If they were "
        "repaired against the scan, update this file and say so; if a blanket sweep removed the "
        "evidence of corruption without fixing it, revert."
    )


def test_the_danda_substitution_survived():
    """19.4's `l` was a mis-OCR'd danda. A later sweep must not turn it back into nothing."""
    text = dict(_verses()).get("19.4", "")
    assert text, "19.4 is missing from the corpus"
    assert "गृहभित्यग्" in text, "19.4 no longer holds its anchor -- the text changed"
    before_anchor = text.split("गृहभित्यग्")[0]
    assert before_anchor.rstrip().endswith("।"), (
        f"19.4 should end the preceding pada with a danda; got {before_anchor[-24:]!r}. "
        "render-193/txt renders this position `नुजले'।`."
    )


#: The nine verses recovered on 2026-09-30 by splitting an OCR-merged pair (G71). Each was
#: created by cutting the verse numbered N+1 at its own `॥ € ॥` / `॥ ॥` -- the lost `॥ ९ ॥`
#: marker, still sitting in the text where the converter failed to read it as a boundary.
SPLIT_RECOVERED = {
    "3.9", "4.9", "5.9", "9.9", "11.9", "12.9", "15.9", "17.9", "20.8",
}


def test_the_ocr_merged_verses_stayed_split():
    """A re-conversion from the same OCR would re-merge these. Fail loudly if it does.

    Eight of the nine are verse NINE, which is the whole point: `॥ ९ ॥` is read 2 times in 336
    pages against 20-28 for its neighbours, so verse 9's closing marker is usually absent and its
    text runs into verse 10. G71.
    """
    verses = dict(_verses())
    missing = sorted(SPLIT_RECOVERED - set(verses))
    assert not missing, (
        f"{len(missing)} verse(s) recovered from an OCR merge are gone again: {missing}. "
        "A re-conversion from the same OCR pass re-merges them -- the split point is the lost "
        "`॥ ९ ॥` marker (G71), not anything the converter can infer."
    )
    #: Each recovered verse must be a real verse body, not a fragment left by a bad cut.
    tiny = {k: len(verses[k]) for k in SPLIT_RECOVERED if len(verses[k]) < 40}
    assert not tiny, f"recovered verses are too short to be verse bodies: {tiny}"


def test_no_recovered_verse_serves_a_translation_it_did_not_earn():
    """The merged translation covered BOTH verses, so neither half may serve it.

    It was demoted to `english_draft`/`hindi_draft` rather than deleted: the work is real, it is
    simply not verified at verse granularity. Leaving it on the first half would make the corpus
    assert that verse 9 says things only verse 10 says.
    """
    import json as _json
    for path in corpus_files(ROOT):
        doc = _json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or doc.get("text_id") != TEXT_ID:
            continue
        for ch in doc["chapters"]:
            for sh in ch.get("shlokas") or []:
                key = f"{ch['number']}.{sh['number']}"
                if key not in SPLIT_RECOVERED:
                    continue
                assert not (sh.get("english") or "").strip(), (
                    f"{key} serves an english that was a translation of a MERGED pair"
                )
                assert sh.get("status") in {"drafted", "untranslated"}, (
                    f"{key} has status {sh.get('status')!r}; it serves no translation"
                )
        return
