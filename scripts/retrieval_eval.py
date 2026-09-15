#!/usr/bin/env python3
"""
Score the frozen 50 pairs in docs/RETRIEVAL_EVAL.md against three retrieval arms.

ANSWERS D2' in docs/EMBEDDING_EVAL.md: "embeddings earn their existence iff they answer
queries the TAG LAYER cannot." The headline is not which arm wins — it is how many of the
50 the TAG ARM already answers, because that is the size of the gap a vector store would
have to fill.

THE ENGLISH->TAG BRIDGE IS THE METHODOLOGICALLY DANGEROUS PART, so it is stated plainly:

The questions are English; the tags were derived from Devanagari. Something must bridge
them. **That bridge is written ONCE, generally, over the measured demand vocabulary — never
per question.** A per-question mapping would be the gold set scoring itself: I would be
encoding the answer and then measuring my own encoding.

So BRIDGE below maps the vocabulary that `marketing-intel`'s GSC classifier and the booking
`life_area` enum actually use — Saturn, Rahu-Ketu, Lagna, Mahadasha, career, money, marriage,
family, health — plus plain ordinals. It is applied identically to all 50, and several
questions get NO tags from it, which is a real result rather than something to patch.

ROW 43 IS A TRAP AND IS SCORED AS ONE. Kala-sarpa is a modern construct with no BPHS verse.
Its gold is empty. An arm that returns a confident answer there scores a FALSE POSITIVE, not
a miss. It is the only row that can be failed by over-answering, and it exists because the
three highest-demand popular terms — sade sati, manglik, kaal sarp — return zero English
matches in the whole text.

Exit codes (rule:discernment-checks §2):
  0  ran, scored
  1  the doc and the corpus disagree — a gold ref that does not exist
  2  could not run — no corpus, no eval doc, or no parseable pairs
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BPHS = REPO / "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json"
DOC = REPO / "docs" / "RETRIEVAL_EVAL.md"

ROW = re.compile(r"^\|\s*(\d+)\s*\|([^|]*)\|([^|]*)\|\s*`?([\d.]+|—)`?\s*\|([^|]*)\|")
REF = re.compile(r"`?([\d]+\.[\d]+[^`\s]*)`?")

# ---------------------------------------------------------------------------
# The bridge. Written once, over the demand vocabulary measured in
# marketing-intel/docs/keyword-demand-direction.md and the booking life_area enum.
# NOT written per question. Several questions get nothing from it — that is a result.
# ---------------------------------------------------------------------------
BRIDGE = {
    # GSC classifier buckets
    "saturn": "graha:saturn", "rahu": "graha:rahu", "ketu": "graha:ketu",
    "sun": "graha:sun", "moon": "graha:moon", "mars": "graha:mars",
    "mercury": "graha:mercury", "jupiter": "graha:jupiter", "venus": "graha:venus",
    "lagna": "bhava:1", "ascendant": "bhava:1",
    "mahadasha": "entity:dasha", "antardasha": "entity:dasha", "dasa": "entity:dasha",
    "dasha": "entity:dasha", "period": "entity:dasha",
    # booking life_area
    "career": "bhava:10", "profession": "bhava:10",
    "money": "bhava:2", "wealth": "bhava:2", "wealthy": "bhava:2", "poverty": "bhava:2",
    "marriage": "bhava:7", "wife": "bhava:7", "spouse": "bhava:7",
    "children": "bhava:5", "sons": "bhava:5", "son": "bhava:5",
    "father": "bhava:9", "mother": "bhava:4", "siblings": "bhava:3", "brothers": "bhava:3",
    "health": "bhava:6", "disease": "bhava:6", "illness": "bhava:6", "leprosy": "bhava:6",
    "longevity": "bhava:8", "long-lived": "bhava:8",
    # ordinals -> bhava
    "first": "bhava:1", "second": "bhava:2", "third": "bhava:3", "fourth": "bhava:4",
    "fifth": "bhava:5", "sixth": "bhava:6", "seventh": "bhava:7", "eighth": "bhava:8",
    "ninth": "bhava:9", "tenth": "bhava:10", "eleventh": "bhava:11", "twelfth": "bhava:12",
    "1st": "bhava:1", "2nd": "bhava:2", "3rd": "bhava:3", "4th": "bhava:4",
    "5th": "bhava:5", "6th": "bhava:6", "7th": "bhava:7", "8th": "bhava:8",
    "9th": "bhava:9", "10th": "bhava:10", "11th": "bhava:11", "12th": "bhava:12",
    # relations
    "lord": "rel:lordship", "exalted": "rel:dignity", "exaltation": "rel:dignity",
    "debilitated": "rel:dignity", "own sign": "rel:dignity",
    "quadrant": "rel:house_group", "trine": "rel:house_group", "kendra": "rel:house_group",
    "aspect": "rel:aspect", "aspected": "rel:aspect",
    "conjoined": "rel:conjunction", "with": None, "associated": "rel:conjunction",
    "malefic": "rel:polarity", "malefics": "rel:polarity", "benefic": "rel:polarity",
    "yoga": "entity:yoga", "raja yoga": "entity:yoga",
}

STOP = set("what does the a an of and or in is are be to for from with how when which "
           "that this it its his her their who do give gives make makes cause causes "
           "person native house planet during inside versus".split())


def parse_pairs(path):
    if not path.exists():
        print(f"could not run: no eval doc at {path}", file=sys.stderr)
        return None
    pairs = []
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        n, slice_, q, gold, also = m.groups()
        golds = [] if gold.strip() == "—" else [gold.strip()]
        golds += REF.findall(also)
        pairs.append({"n": int(n), "slice": slice_.strip().strip("*"),
                      "q": q.strip(), "gold": golds})
    return pairs or None


def tags_for(question):
    """Apply the bridge. Longest key first so `own sign` beats `sign`."""
    q = question.lower()
    out = set()
    for k in sorted(BRIDGE, key=len, reverse=True):
        if BRIDGE[k] and re.search(rf"\b{re.escape(k)}\b", q):
            out.add(BRIDGE[k])
    return out


def rank_tags(verses, want):
    """Rank by how many wanted tags a verse carries. No tags wanted -> no answer."""
    if not want:
        return []
    scored = []
    for ref, s in verses:
        have = set(s.get("tags") or [])
        hit = len(want & have)
        if hit:
            scored.append((hit / len(want), -len(have), ref))
    scored.sort(reverse=True)
    return [r for _, _, r in scored]


def rank_text(verses, question):
    """Keyword overlap over english — a $text stand-in, same scoring shape."""
    terms = {w for w in re.findall(r"[a-z0-9]+", question.lower()) if w not in STOP and len(w) > 2}
    if not terms:
        return []
    scored = []
    for ref, s in verses:
        e = (s.get("english") or "").lower()
        hit = sum(1 for t in terms if t in e)
        if hit:
            scored.append((hit / len(terms), len(e) and -len(e), ref))
    scored.sort(reverse=True)
    return [r for _, _, r in scored]


def score(pairs, verses, arm):
    at1 = at5 = miss = fp = 0
    rows = []
    for p in pairs:
        ranked = arm(verses, p)
        trap = not p["gold"]
        if trap:
            bad = bool(ranked)
            fp += bad
            rows.append((p["n"], "FALSE-POSITIVE" if bad else "correctly silent", ""))
            continue
        pos = next((i for i, r in enumerate(ranked) if r in p["gold"]), None)
        if pos == 0:
            at1 += 1; at5 += 1; v = "hit@1"
        elif pos is not None and pos < 5:
            at5 += 1; v = f"hit@5 (#{pos+1})"
        else:
            miss += 1; v = "miss" if ranked else "no answer"
        rows.append((p["n"], v, ranked[0] if ranked else ""))
    return {"at1": at1, "at5": at5, "miss": miss, "fp": fp, "rows": rows}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--verbose", action="store_true", help="print every row")
    args = ap.parse_args()

    pairs = parse_pairs(DOC)
    if pairs is None:
        return 2
    try:
        doc = json.loads(BPHS.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2
    verses = [(f"{c['number']}.{s['number']}", s)
              for c in doc["chapters"] for s in c["shlokas"]]
    index = {r for r, _ in verses}

    bad = [g for p in pairs for g in p["gold"] if g not in index]
    if bad:
        print(f"the doc names {len(bad)} gold ref(s) the corpus does not have: {bad[:6]}",
              file=sys.stderr)
        return 1

    n = len(pairs)
    traps = sum(1 for p in pairs if not p["gold"])
    print(f"  {n} pairs · {n-traps} scorable · {traps} trap (no valid answer exists)")
    print(f"  corpus: {len(verses):,} verses, "
          f"{sum(1 for _, s in verses if s.get('tags')):,} tagged")
    print()

    arms = {
        "tags": lambda v, p: rank_tags(v, tags_for(p["q"])),
        "$text": lambda v, p: rank_text(v, p["q"]),
    }
    res = {}
    print(f"  {'arm':<8}{'hit@1':>7}{'hit@5':>7}{'miss':>7}{'false-pos':>11}")
    print("  " + "-" * 40)
    for name, fn in arms.items():
        r = score(pairs, verses, fn)
        res[name] = r
        print(f"  {name:<8}{r['at1']:>7}{r['at5']:>7}{r['miss']:>7}{r['fp']:>11}")
    print("  " + "-" * 40)
    print(f"  of {n-traps} scorable, the TAG arm answers {res['tags']['at5']} in its top five")
    print(f"  ({100*res['tags']['at5']/(n-traps):.0f}%) — that is the gap an embedding must fill")
    print()
    print("  embeddings arm: NOT RUN (needs an API key). Absent, not zero.")

    if args.verbose:
        for name, r in res.items():
            print(f"\n  --- {name}")
            for num, v, top in r["rows"]:
                p = next(x for x in pairs if x["n"] == num)
                print(f"    {num:>3} {v:<18}{top:<9}{p['q'][:54]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
