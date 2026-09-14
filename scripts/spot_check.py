#!/usr/bin/env python3
"""
Build — and later score — the stratified manual spot-check of the feature tags.

Step 5. THIS IS THE ONLY HONEST PRECISION ESTIMATE AVAILABLE, and it needs a human who
reads Sanskrit. Nothing here substitutes for that; this file only makes the reading
cheap and makes the result a number rather than an impression.

WHY NOT AN AUTOMATED ORACLE. Two were tried in this project and both were circular:
an English-agreement rate that measured agreement conditional on agreement, and a
"100% Vimsottari" that assigned labels by walking Vimsottari order. A third — the
chapter-position check in entity_roots.py — IS sound, but it validates the CHAIN
EXTRACTION against the book's own organisation, not per-tag precision. Those are
different claims. This file answers the second one and only the second one.

TWO MODES, the generated/curated split this repo uses throughout:

  (default)  write docs/SPOT_CHECK.md — the sample and an empty verdict column
  --score    read the filled-in verdict column back and report precision per tag type

SAMPLING IS DETERMINISTIC. A fixed seed over a sorted verse list, so re-running
reproduces the same sample and a reviewer's half-finished sheet is never invalidated.
Stratified by chapter — 20 chapters spread across the book, 10 verses each — because
tag density varies enormously by subject and an unstratified draw would over-sample
the bhava chapters.

Exit codes (rule:discernment-checks §2):
  0  ran
  1  --score found no verdicts to score, or the sheet disagrees with the corpus
  2  could not run — corpus absent or unparseable
"""

import argparse
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BPHS = REPO / "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json"
SHEET = REPO / "docs" / "SPOT_CHECK.md"

SEED = 20260914          # the date, so the sample is reproducible and its origin is legible
N_CHAPTERS = 20
PER_CHAPTER = 10
VERDICTS = {"ok", "wrong", "partial", "unsure"}

ROW = re.compile(r"^\|\s*`(\d+)\.([^`]+)`\s*\|")


def sample(doc):
    """Deterministic stratified draw. Returns [(chapter, shloka_obj)]."""
    tagged = defaultdict(list)
    for ch in doc.get("chapters") or []:
        for sh in ch.get("shlokas") or []:
            if sh.get("tags"):
                tagged[ch["number"]].append(sh)
    if not tagged:
        return None
    rng = random.Random(SEED)
    chapters = sorted(tagged, key=lambda c: str(c))
    # spread across the book rather than taking a contiguous block
    step = max(1, len(chapters) // N_CHAPTERS)
    picked = chapters[::step][:N_CHAPTERS]
    out = []
    for c in picked:
        verses = sorted(tagged[c], key=lambda s: str(s["number"]))
        out += [(c, s) for s in rng.sample(verses, min(PER_CHAPTER, len(verses)))]
    return out


def read_verdicts(path):
    """{(chapter, shloka): (verdict, note)} from a filled-in sheet."""
    if not path.exists():
        return {}
    got = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5:
            continue
        v = cells[3].strip().lower()
        if v in VERDICTS:
            got[(m.group(1), m.group(2))] = (v, cells[4])
    return got


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--score", action="store_true",
                    help="read the filled-in sheet and report precision instead of writing it")
    args = ap.parse_args()

    if not BPHS.exists():
        print(f"could not run: {BPHS} does not exist", file=sys.stderr)
        return 2
    try:
        doc = json.loads(BPHS.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"could not run: {BPHS} does not parse: {e}", file=sys.stderr)
        return 2

    rows = sample(doc)
    if rows is None:
        print("could not run: no tagged verses — run tag_features.py --apply first",
              file=sys.stderr)
        return 2

    if args.score:
        got = read_verdicts(SHEET)
        if not got:
            print(f"could not score: no verdicts filled in at {SHEET}\n"
                  f"  the verdict column must read one of: {', '.join(sorted(VERDICTS))}",
                  file=sys.stderr)
            return 1
        tally = Counter(v for v, _ in got.values())
        by_type = defaultdict(Counter)
        for (c, s), (v, _) in got.items():
            sh = next((x for ch in doc["chapters"] if str(ch["number"]) == c
                       for x in ch["shlokas"] if str(x["number"]) == s), None)
            for t in (sh.get("tags") if sh else []) or []:
                by_type[t.split(":")[0]][v] += 1
        n = len(got)
        print(f"  {n} of {len(rows)} sampled verses reviewed ({100*n/len(rows):.0f}%)")
        for v in sorted(VERDICTS):
            print(f"    {v:<9}{tally[v]:>5}  {100*tally[v]/n:>5.1f}%")
        judged = tally["ok"] + tally["wrong"] + tally["partial"]
        if judged:
            print(f"\n  precision (ok / ok+wrong+partial): {100*tally['ok']/judged:.1f}%")
            print(f"  'unsure' is EXCLUDED from that denominator and reported separately —")
            print(f"  folding it either way would invent a verdict the reviewer withheld.")
        print("\n  by tag type:")
        for t, c in sorted(by_type.items(), key=lambda kv: -sum(kv[1].values())):
            tot = c["ok"] + c["wrong"] + c["partial"]
            p = f"{100*c['ok']/tot:.0f}%" if tot else "n/a"
            print(f"    {t:<10}{sum(c.values()):>5} tags · ok {c['ok']:>4} · wrong {c['wrong']:>4} · {p}")
        return 0

    prior = read_verdicts(SHEET)          # never lose a reviewer's work on regeneration
    lines = [
        "# Spot check — the only honest precision estimate",
        "",
        "**Generated by `scripts/spot_check.py`. The `verdict` and `note` columns are CURATED",
        "and survive regeneration; everything else is overwritten.**",
        "",
        "This needs a reader of Sanskrit. No automated oracle in this project can replace it:",
        "two were tried and both were circular, and the one sound automated check validates the",
        "*chain extraction* against chapter organisation, not per-tag precision.",
        "",
        "## How to review",
        "",
        "For each row, read the Devanāgarī and judge **the tags**, not the translation.",
        "Write one word in `verdict`:",
        "",
        "| verdict | means |",
        "|---|---|",
        "| `ok` | every tag on this verse is right |",
        "| `wrong` | at least one tag is wrong |",
        "| `partial` | tags are right but something obvious is missed |",
        "| `unsure` | cannot judge — **use this freely**; it is reported separately and never",
        "folded into precision either way |",
        "",
        "Put what was wrong in `note`. Then: `python3 scripts/spot_check.py --score`.",
        "",
        f"Sample: **{len(rows)} verses across {len({c for c, _ in rows})} chapters**, drawn",
        f"deterministically (seed {SEED}) and stratified by chapter, because tag density varies",
        "by subject and an unstratified draw over-samples the bhāva chapters.",
        "",
        "## Sample",
        "",
        "| ref | devanāgarī | tags | verdict | note |",
        "|---|---|---|---|---|",
    ]
    for c, sh in rows:
        key = (str(c), str(sh["number"]))
        v, note = prior.get(key, ("", ""))
        dev = (sh.get("text", "") or "").replace("\n", " ").replace("|", "/")[:110]
        tags = " ".join(f"`{t}`" for t in sorted(sh.get("tags") or []))
        lines.append(f"| `{c}.{sh['number']}` | {dev} | {tags} | {v} | {note} |")
    lines.append("")

    SHEET.parent.mkdir(parents=True, exist_ok=True)
    SHEET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {len(rows)} verses across {len({c for c, _ in rows})} chapters")
    print(f"  {len(prior)} existing verdict(s) carried forward")
    print(f"-> {SHEET.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
