#!/usr/bin/env python3
"""
Tag every shloka with the entities and relations it names.

Steps 3 and 4 of the feature plan, together, because the write guard is not a separate
pass — it is the only thing standing between a matcher bug and a corrupted corpus.

VOCABULARY IS NOT DEFINED HERE. The roots live in docs/ENTITY_ROOTS.md and the markers
in docs/RELATION_MARKERS.md, both curated; this file imports their parsers rather than
carrying a third copy, because three copies of one list is how a rule ends up with four
mutually exclusive versions of itself.

THE MATCHER IS MAXIMAL MUNCH, AND PER-TOKEN "PICK THE LONGEST" WOULD BE WRONG.
Measured 2026-09-14: 24 distinct tokens name MORE THAN ONE entity —
`चन्द्रसूर्यग्रहे` is Moon and Sun, `शनिचन्द्रबुधा` is Saturn, Moon and Mercury,
`राहुश्चन्द्रसूर्ययुतो` is three grahas plus a conjunction marker. Choosing one root
per token would discard the rest. So the scan walks the token left to right, takes the
LONGEST root matching at each position, emits it, and advances past it.

That same rule solves the patronymic trap structurally, with no exclusion needed: at
position 0 of `सोमसुतस्य`, `सोमसुत` (Mercury) is longer than `सोम` (Moon) and wins.
`सूर्यज`/`भानुज` beat `सूर्य`/`भानु` the same way. The exclusion lists remain for the
cases longest-match CANNOT fix — `देश` is not a longer form of `ेश`, it merely contains
it — and the two mechanisms are doing genuinely different jobs.

BHAVA IS STRICT. A bhava root tags only when the token also carries a lord-suffix, a
locative, or a position marker, because the 2nd house IS dhana and `धनं लभते` ("obtains
wealth") is a phala, not a house. Loose tagging would have doubled the bhava count.

Exit codes (rule:discernment-checks §2):
  0  ran
  1  refused — the key set moved, or a written file failed to re-parse
  2  could not run — corpus, doc, or text_id absent
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import entity_roots as ER          # noqa: E402  — parsers, not a copy of the lists
import relation_markers as RM      # noqa: E402

REPO = Path(__file__).resolve().parent.parent
WORD = re.compile(r"[ऀ-ॣ॰-ॿ]+")

# Tag slugs match astroacharya/seeds/*.json so a tag joins to its entity table with no
# translation step. Bhavas are numbered there, so they are numbered here.
GRAHA_SLUG = {
    "सूर्य": "sun", "रवि": "sun", "भास्कर": "sun", "भानु": "sun",
    "दिवानाथ": "sun", "दिवाकर": "sun",
    "चन्द्र": "moon", "शशि": "moon", "विधु": "moon", "इन्दु": "moon", "सोम": "moon",
    "हिमांशु": "moon", "कुमुद": "moon",
    "कुज": "mars", "भौम": "mars", "मङ्गल": "mars", "अङ्गारक": "mars", "रुधिर": "mars",
    "भूसुत": "mars", "भूपुत्र": "mars",
    "बुध": "mercury", "सोमसुत": "mercury", "धरात्मज": "mercury",
    "जीव": "jupiter", "बृहस्पति": "jupiter", "देवेज्य": "jupiter", "गुरु": "jupiter",
    "शुक्र": "venus", "भृगु": "venus", "भार्गव": "venus",
    "शनि": "saturn", "मन्द": "saturn", "सूर्यज": "saturn", "अर्कज": "saturn",
    "छायासूनु": "saturn", "सौरि": "saturn", "भानुज": "saturn",
    "राहु": "rahu", "राहो": "rahu", "स्वर्भानु": "rahu",
    "केतु": "ketu", "केतो": "ketu", "शिखि": "ketu",
}
RASHI_SLUG = {"मेष": "mesha", "वृष": "vrishabha", "मिथुन": "mithuna", "कर्क": "karka",
              "सिंह": "simha", "कन्या": "kanya", "तुला": "tula", "वृश्चिक": "vrischika",
              "धनु": "dhanus", "मकर": "makara", "कुम्भ": "kumbha", "मीन": "mina"}
BHAVA_NUM = {"लग्न": 1, "धन": 2, "सहज": 3, "भ्रातृ": 3, "सुख": 4, "वाहन": 4, "मातृ": 4,
             "सुत": 5, "पुत्र": 5, "पञ्चम": 5, "षष्ठ": 6, "रिपु": 6, "अरि": 6, "दार": 7,
             "द्यून": 7, "जाया": 7, "सप्तम": 7, "रन्ध्र": 8, "अष्टम": 8, "भाग्य": 9,
             "धर्म": 9, "पितृ": 9, "कर्म": 10, "राज्य": 10, "लाभ": 11, "व्यय": 12}

TAG_RE = re.compile(r"^(graha|rashi|bhava|entity|rel|chain|mahadasha):[a-z_0-9]+$")

# A flat tag SET cannot represent a proposition, and that is measured rather than feared:
# 38 (lord_of, in_house) pairs occur in BPHS together with their reverse, and
# `सुतेशे भाग्यगे` (lord of 5 in 9) and `भाग्येशो … सुतेशो` (lord of 9 in 5) produce the
# SAME set. 20% of tagged verses share their tag set with another verse.
#
# The fix keeps the binding INSIDE the tag string — `chain:lord5_pos9` — rather than adding
# a structured field. That matters: `_normalize_shloka` in astroacharya is a 12-key
# ALLOWLIST (G50), so a new key would not reach Mongo at all without a two-repo change to
# the same allowlist that guards the publication gate. A tag string needs neither.
CHAIN_SUBJ = ("bhava:", "graha:")
# Written by tag_dashas.py, not by this script — preserved verbatim. Everything else
# under the tags key is this script's output and is regenerated from scratch each run.
OWNED_BY_OTHERS = ("mahadasha:",)


def build_lexicon():
    """One {root: tag} map over both curated docs, or (None, reason)."""
    roots, _, e_excl = ER.parse_doc(ER.DOC)
    if roots is None:
        return None, None, "entity doc unparseable"
    concepts, _, r_excl = RM.load_markers(RM.DOC)
    if concepts is None:
        return None, None, "marker doc unparseable"
    roots.pop("any entity", None)

    lex = {}
    for kind, rs in roots.items():
        for r in rs:
            if kind == "GRAHA":
                lex[r] = f"graha:{GRAHA_SLUG[r]}" if r in GRAHA_SLUG else None
            elif kind == "RASHI":
                lex[r] = f"rashi:{RASHI_SLUG[r]}" if r in RASHI_SLUG else None
            elif kind == "BHAVA":
                lex[r] = f"bhava:{BHAVA_NUM[r]}" if r in BHAVA_NUM else "entity:bhava"
            else:
                lex[r] = f"entity:{kind.lower()}"
    for concept, ms in concepts.items():
        for m in ms:
            lex.setdefault(m, f"rel:{concept.lower()}")
    lex = {k: v for k, v in lex.items() if v}

    excl = dict(e_excl)
    for k, v in r_excl.items():
        excl.setdefault(k, []).extend(v)
    return lex, excl, None


def scan(word, lex, order, excl):
    """Maximal munch over one token. Returns the set of tags it carries.

    Left to right; at each position the LONGEST root wins and the cursor jumps past it.
    That is what lets one token yield Saturn AND Moon AND Mercury, and what makes
    सोमसुत beat सोम without an exclusion entry.
    """
    out, i, n = set(), 0, len(word)
    while i < n:
        for r in order:
            if len(r) > n - i or not word.startswith(r, i):
                continue
            if RM.blocked(word, r, excl):
                continue
            tag = lex[r]
            if tag.startswith("bhava:") or tag == "entity:bhava":
                if not ER.bhava_house_sense(word, r):   # strict: house, not phala
                    continue
            out.add(tag)
            i += len(r) - 1
            break
        i += 1
    return out


def chains(seq):
    """Ordered (subject, position) pairs from the token sequence.

    A token carrying a subject AND lordship is a lord-subject (`सुतेशे` -> lord of 5); a
    token carrying a subject AND position is a locus (`भाग्यगे` -> in 9). Emitting the
    pair in ORDER is the whole point — it is what distinguishes lord(5)-in-9 from
    lord(9)-in-5, which the flat set cannot.
    """
    out, subj = set(), None
    for tags in seq:
        ents = [t for t in tags if t.startswith(CHAIN_SUBJ)]
        if not ents:
            continue
        ent = sorted(ents)[0]
        kind, val = ent.split(":", 1)
        if "rel:lordship" in tags:
            subj = f"lord{val}" if kind == "bhava" else val
        elif "rel:position" in tags and subj:
            out.add(f"chain:{subj}_pos{val}" if kind == "bhava" else f"chain:{subj}_with_{val}")
            subj = None
        elif kind == "graha" and "rel:lordship" not in tags:
            subj = val
    return out


def key_set(doc):
    """Every (chapter, shloka). A SET, never a count — a pass that drops one verse and
    adds another survives a length check, which is how dhanurveda went 227 -> 2."""
    return {(c["number"], s["number"]) for c in doc["chapters"] for s in c["shlokas"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--text", default="bphs",
                    help="text_id to tag (default bphs — the roots were derived from it)")
    ap.add_argument("--apply", action="store_true",
                    help="write the file; without it NOTHING is written")
    args = ap.parse_args()

    lex, excl, why = build_lexicon()
    if lex is None:
        print(f"could not run: {why}", file=sys.stderr)
        return 2
    order = sorted(lex, key=len, reverse=True)      # longest first == maximal munch

    doc, rel = ER.load_text(args.text)
    if doc is None:
        print(f"could not run: no text with text_id '{args.text}' under {REPO}", file=sys.stderr)
        return 2
    path = REPO / rel
    before = key_set(doc)

    tally, tagged, added = Counter(), 0, 0
    for ch in doc["chapters"]:
        for sh in ch["shlokas"]:
            found, seq = set(), []
            for w in WORD.findall(sh.get("text", "")):
                tags = scan(w, lex, order, excl)
                found |= tags
                if tags:
                    seq.append(tags)
            found |= chains(seq)
            if found:
                tagged += 1
            for t in found:
                tally[t] += 1
            # Keep ONLY tags this script does not own; REPLACE the ones it does.
            # Merging instead would make the tagger non-idempotent under vocabulary
            # change: a root removed from the curated doc would leave its tags behind
            # forever, so the corpus would be the union of every vocabulary ever used.
            # That is the "seeder never deletes" defect, one layer down — caught when
            # excluding जीव from Jupiter left verse 1.21 still tagged graha:jupiter.
            keep = [t for t in (sh.get("tags") or []) if t.startswith(OWNED_BY_OTHERS)]
            merged = sorted(set(keep) | found)
            if merged != (sh.get("tags") or []):
                sh["tags"] = merged
                added += 1

    if key_set(doc) != before:
        print("REFUSING — the key set moved during tagging", file=sys.stderr)
        return 1

    n = sum(len(c["shlokas"]) for c in doc["chapters"])
    print(f"{args.text}  ({rel})  {n:,} verses · {len(lex)} roots")
    print(f"  verses receiving >=1 tag : {tagged:,}  ({100*tagged/n:.1f}%)")
    print(f"  verses whose tags change : {added:,}")
    print(f"  distinct tags            : {len(tally)}")
    for t, c in tally.most_common(12):
        print(f"      {c:>5}  {t}")

    if not args.apply:
        print("  DRY RUN — nothing written. Re-run with --apply.")
        return 0

    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reread = json.loads(path.read_text(encoding="utf-8"))
    if key_set(reread) != before:
        print("WROTE A FILE WHOSE KEY SET MOVED — restore from git", file=sys.stderr)
        return 1
    print("  WRITTEN and re-parsed OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
