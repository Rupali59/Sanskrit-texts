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


def phala_sample(doc, per_chapter=12):
    """Every chapter that has been READ, up to `per_chapter` verses each.

    Drawn separately from the matched-tag sample because the two layers are different
    KINDS of claim and need different judgements. A `graha:mars` tag is a string match
    and is right or wrong about the text. A `phala:wealth` tag is a READING, and its
    failure mode is a defensible-but-different category, not a mismatch. Folding them
    into one verdict column would average two unlike things.
    """
    read = defaultdict(list)
    for ch in doc.get("chapters") or []:
        for sh in ch.get("shlokas") or []:
            if sh.get("tags_draft"):
                read[ch["number"]].append(sh)
    if not read:
        return []
    rng = random.Random(SEED)
    out = []
    for c in sorted(read, key=lambda x: str(x)):
        verses = sorted(read[c], key=lambda s: str(s["number"]))
        out += [(c, s) for s in rng.sample(verses, min(per_chapter, len(verses)))]
    return out


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


PHALA_HEADING = "## Phala sample"


def read_verdicts(path):
    """{(section, chapter, shloka): (verdict, note)} from a filled-in sheet.

    KEYED BY SECTION, and that is not cosmetic: 42 verses appear in BOTH samples, so a
    key of (chapter, shloka) alone would let a verdict written in one section silently
    overwrite the reviewer's verdict for the same verse in the other. Their two
    judgements are about different tags and must not collide.

    Section is decided by position — every row after the phala heading belongs to it.
    """
    if not path.exists():
        return {}
    got = {}
    section = "tags"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith(PHALA_HEADING):
            section = "phala"
            continue
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        # the phala table has an extra `english` column, so the verdict sits one later
        idx = 4 if section == "phala" else 3
        if len(cells) < idx + 2:
            continue
        v = cells[idx].strip().lower()
        if v in VERDICTS:
            got[(section, m.group(1), m.group(2))] = (v, cells[idx + 1])
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
        ph_rows = phala_sample(doc)
        sizes = {"tags": len(rows), "phala": len(ph_rows)}
        field = {"tags": "tags", "phala": "tags_draft"}
        # NEVER pool the two. They are different kinds of claim scored against different
        # instructions, and one precision number over both would be a mixture reported as
        # a measurement (rule:discernment-checks §5).
        for section in ("tags", "phala"):
            sub = {k: v for k, v in got.items() if k[0] == section}
            print(f"\n  === {section} layer")
            if not sub:
                print(f"    not reviewed yet — 0 of {sizes[section]}")
                continue
            tally = Counter(v for v, _ in sub.values())
            by_type = defaultdict(Counter)
            for (_, c, s), (v, _) in sub.items():
                sh = next((x for ch in doc["chapters"] if str(ch["number"]) == c
                           for x in ch["shlokas"] if str(x["number"]) == s), None)
                for t in (sh.get(field[section]) if sh else []) or []:
                    by_type[t.split(":")[0]][v] += 1
            n = len(sub)
            print(f"    {n} of {sizes[section]} reviewed ({100*n/max(sizes[section],1):.0f}%)")
            for v in sorted(VERDICTS):
                print(f"      {v:<9}{tally[v]:>5}  {100*tally[v]/n:>5.1f}%")
            judged = tally["ok"] + tally["wrong"] + tally["partial"]
            if judged:
                print(f"    precision (ok / ok+wrong+partial): {100*tally['ok']/judged:.1f}%")
            for t, c in sorted(by_type.items(), key=lambda kv: -sum(kv[1].values())):
                tot = c["ok"] + c["wrong"] + c["partial"]
                pc = f"{100*c['ok']/tot:.0f}%" if tot else "n/a"
                print(f"      {t:<10}{sum(c.values()):>5} tags · ok {c['ok']:>4} · wrong {c['wrong']:>4} · {pc}")
        print("\n  'unsure' is EXCLUDED from every precision denominator and reported")
        print("  separately — folding it either way invents a verdict the reviewer withheld.")
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
        "| `unsure` | cannot judge — **use this freely**; reported separately, never folded in |",
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
        key = ("tags", str(c), str(sh["number"]))
        v, note = prior.get(key, ("", ""))
        dev = (sh.get("text", "") or "").replace("\n", " ").replace("|", "/")[:110]
        tags = " ".join(f"`{t}`" for t in sorted(sh.get("tags") or []))
        lines.append(f"| `{c}.{sh['number']}` | {dev} | {tags} | {v} | {note} |")
    lines.append("")

    ph = phala_sample(doc)
    if ph:
        lines += [
            "",
            "## Phala sample — a DIFFERENT judgement, please read this first",
            "",
            "These carry `phala:` tags in `tags_draft`. They were assigned by **reading the",
            "verse**, not by matching strings, because the result side of a shloka has no",
            "productive morphology to match on.",
            "",
            "**So judge them differently.** For the sample above, a tag is right or wrong about",
            "the text. Here, the common failure is a *defensible but different* category —",
            "`phala:loss` where you would have said `phala:sorrow`. That is not `wrong`.",
            "",
            "| verdict | means, for THIS section |",
            "|---|---|",
            "| `ok` | you would accept every tag, even if you might have added others |",
            "| `wrong` | a tag is not supported by the verse at all |",
            "| `partial` | a clear result the verse states is missing |",
            "| `unsure` | cannot judge |",
            "",
            "The 18 categories and the rule for each are in",
            "[`PHALA_CATEGORIES.md`](PHALA_CATEGORIES.md). Two are worth knowing before you",
            "start: a category is the **topic**, so `phala:wealth` covers a verse about the loss",
            "of wealth too; and verses that state no result at all — chapter openings,",
            "methodological closers — correctly carry **no** phala tag.",
            "",
            f"Sample: **{len(ph)} verses across {len({c for c, _ in ph})} chapters** of the",
            f"{sum(1 for c in doc['chapters'] for s in c['shlokas'] if s.get('tags_draft'))} read so far.",
            "",
            "| ref | devanāgarī | english | phala | verdict | note |",
            "|---|---|---|---|---|---|",
        ]
        for c, sh in ph:
            key = ("phala", str(c), str(sh["number"]))
            v, note = prior.get(key, ("", ""))
            dev = (sh.get("text", "") or "").replace("\n", " ").replace("|", "/")[:78]
            eng = (sh.get("english", "") or "").replace("\n", " ").replace("|", "/")[:88]
            tags = " ".join(f"`{x.split(':', 1)[1]}`" for x in sorted(sh.get("tags_draft") or [])
                            if x.startswith("phala:")) or "*(none — states no result)*"
            lines.append(f"| `{c}.{sh['number']}` | {dev} | {eng} | {tags} | {v} | {note} |")
        lines.append("")

    SHEET.parent.mkdir(parents=True, exist_ok=True)
    SHEET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"  {len(rows)} verses across {len({c for c, _ in rows})} chapters (matched tags)")
    print(f"  {len(ph)} verses across {len({c for c, _ in ph})} chapters (read phala)")
    print(f"  {len(prior)} existing verdict(s) carried forward")
    print(f"-> {SHEET.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
