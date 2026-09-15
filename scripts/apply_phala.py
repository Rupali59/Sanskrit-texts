#!/usr/bin/env python3
"""
Apply READ phala tags to the corpus — into `tags_draft`, never into `tags`.

THE DIVISION OF LABOUR IS THE POINT. The phala layer is assigned by reading each verse,
because the result side of a shloka has no productive morphology to match on (measured:
adjacency to a result verb covers 761 of 3,937 verses and returns `च`, `वा`, `तु`). So the
READING is done by a language model and the WRITING is done here, where it can be guarded.

This script therefore never decides anything semantic. It validates against the closed
category set in docs/PHALA_CATEGORIES.md, refuses anything not on it, and writes with the
same guards every other writer in this repo uses.

WHY `tags_draft` AND NOT `tags`. The workspace hard rule is "Computation is AI-assisted;
meaning is not." A matched tag ("this verse contains धनेशे") is computation. A READ tag
("this verse predicts wealth") is closer to meaning — and `tags` IS one of the 12 keys in
astroacharya's `_normalize_shloka` allowlist, so it reaches the public API.

`tags_draft` is NOT in that allowlist, so it is structurally unable to reach the API. Same
gate that has always protected `english_draft`; no new mechanism; G50 untouched. Promotion
into `tags` is a separate, human act.

INPUT is JSON: {"<chapter>.<shloka>": {"phala": ["wealth", ...], "align": "aligned"}}
`phala` may be empty — that is a real assignment meaning "this verse states no result".

Exit codes (rule:discernment-checks §2):
  0  ran
  1  refused — unknown category, unknown verse, or the key set moved
  2  could not run — corpus, category doc, or assignment file absent/unparseable
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BPHS = REPO / "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json"
DOC = REPO / "docs" / "PHALA_CATEGORIES.md"

CAT_ROW = re.compile(r"^\|\s*`phala:([a-z_]+)`\s*\|")
ALIGN = {"aligned", "mismatch", "stub", "absent"}


def load_categories(path):
    if not path.exists():
        print(f"could not run: no category doc at {path}", file=sys.stderr)
        return None
    cats = {m.group(1) for line in path.read_text(encoding="utf-8").splitlines()
            if (m := CAT_ROW.match(line))}
    if not cats:
        print(f"could not run: parsed {path} but found no `phala:` category rows",
              file=sys.stderr)
        return None
    return cats


def key_set(doc):
    """(chapter, shloka) as a SET, never a count — a pass that drops one verse and adds
    another survives a length check (G8's mirror; dhanurveda went 227 -> 2 that way)."""
    return {(c["number"], s["number"]) for c in doc["chapters"] for s in c["shlokas"]}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("assignments", help="JSON file of read assignments")
    ap.add_argument("--apply", action="store_true",
                    help="write the file; without it NOTHING is written")
    args = ap.parse_args()

    cats = load_categories(DOC)
    if cats is None:
        return 2
    src = Path(args.assignments)
    if not src.exists():
        print(f"could not run: no assignment file at {src}", file=sys.stderr)
        return 2
    try:
        given = json.loads(src.read_text(encoding="utf-8"))
        doc = json.loads(BPHS.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2

    before = key_set(doc)
    index = {f"{c['number']}.{s['number']}": s
             for c in doc["chapters"] for s in c["shlokas"]}

    # Validate EVERYTHING before writing anything. A partial application would leave the
    # corpus in a state no rerun reproduces.
    problems = []
    for ref, a in given.items():
        if ref not in index:
            problems.append(f"{ref}: no such verse")
            continue
        if not isinstance(a, dict):
            problems.append(f"{ref}: expected an object")
            continue
        for p in a.get("phala", []):
            if p not in cats:
                problems.append(f"{ref}: `{p}` is not in docs/PHALA_CATEGORIES.md")
        if a.get("align") not in ALIGN:
            problems.append(f"{ref}: align must be one of {sorted(ALIGN)}, got {a.get('align')!r}")
    if problems:
        print(f"REFUSING — {len(problems)} problem(s), nothing written:", file=sys.stderr)
        for p in problems[:15]:
            print(f"  {p}", file=sys.stderr)
        return 1

    tally, align_tally, changed = Counter(), Counter(), 0
    for ref, a in given.items():
        sh = index[ref]
        new = sorted({f"phala:{p}" for p in a.get("phala", [])}
                     | {f"align:{a['align']}"})
        for t in new:
            (align_tally if t.startswith("align:") else tally)[t] += 1
        # OWN and REGENERATE, never merge — a category removed from the doc must leave the
        # corpus, or `tags_draft` becomes the union of every vocabulary ever applied (G52).
        if sh.get("tags_draft") != new:
            sh["tags_draft"] = new
            changed += 1

    if key_set(doc) != before:
        print("REFUSING — the key set moved", file=sys.stderr)
        return 1

    print(f"  assignments read : {len(given)}")
    print(f"  verses changed   : {changed}")
    print(f"  phala tags       : {sum(tally.values())} across {len(tally)} categories")
    for t, n in tally.most_common():
        print(f"      {n:>4}  {t}")
    print("  alignment verdicts:")
    for t, n in align_tally.most_common():
        print(f"      {n:>4}  {t}")

    if not args.apply:
        print("  DRY RUN — nothing written. Re-run with --apply.")
        return 0

    BPHS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reread = json.loads(BPHS.read_text(encoding="utf-8"))
    if key_set(reread) != before:
        print("WROTE A FILE WHOSE KEY SET MOVED — restore from git", file=sys.stderr)
        return 1
    print("  WRITTEN to tags_draft and re-parsed OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
