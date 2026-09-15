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
PLANT_CACHE = Path.home() / ".cache" / "sanskrit-texts"

# Deliberately wrong tags, planted to measure whether a REVIEWER is reading the text.
# Every other check in this repo has been held to "construct the input that makes it
# fail"; the reviewer is the one instrument that never has been. A reviewer that misses
# these is not usable, whatever its agreement rate on everything else.
#
# Planted in the RENDERED SHEET ONLY. The corpus is never touched, so there is nothing to
# undo and no path by which a planted defect reaches `tags`.
GRAHA_SWAP = {"sun": "saturn", "moon": "mars", "mars": "moon", "mercury": "venus",
              "jupiter": "rahu", "venus": "mercury", "saturn": "sun", "rahu": "ketu",
              "ketu": "jupiter"}
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


def plant(rows, ph_rows, n, seed):
    """Choose n rows and mutate their rendered tags. Returns {(section, ref): record}.

    Five defect types, each failing a different way — see the plan. The chain reversal is
    the one that matters: 38 (lord_of, in_house) pairs genuinely occur with their reverse
    in BPHS, so a reviewer who cannot catch lord5_pos9 rendered as lord9_pos5 cannot
    validate the only layer that distinguishes them.
    """
    rng = random.Random(seed)
    pool = ([("tags", c, s, sorted(s.get("tags") or [])) for c, s in rows]
            + [("phala", c, s, sorted(x for x in (s.get("tags_draft") or [])
                                      if x.startswith("phala:"))) for c, s in ph_rows])
    pool = [x for x in pool if x[3]]
    rng.shuffle(pool)
    out = {}
    for section, c, sh, tags in pool:
        if len(out) >= n:
            break
        ref = f"{c}.{sh['number']}"
        kinds = []
        if any(x.startswith("chain:lord") and "_pos" in x for x in tags):
            kinds.append("chain_reversed")
        if any(x.startswith("graha:") for x in tags):
            kinds.append("graha_swapped")
        if any(x.startswith("bhava:") for x in tags):
            kinds.append("bhava_swapped")
        kinds += ["tag_added", "tag_dropped"]
        kind = rng.choice(kinds)
        new = list(tags)

        if kind == "chain_reversed":
            i = next(i for i, x in enumerate(new)
                     if x.startswith("chain:lord") and "_pos" in x)
            lord, pos = new[i][len("chain:lord"):].split("_pos", 1)
            new[i] = f"chain:lord{pos}_pos{lord}"
        elif kind == "graha_swapped":
            i = next(i for i, x in enumerate(new) if x.startswith("graha:"))
            g = new[i].split(":", 1)[1]
            new[i] = f"graha:{GRAHA_SWAP.get(g, 'saturn')}"
        elif kind == "bhava_swapped":
            i = next(i for i, x in enumerate(new) if x.startswith("bhava:"))
            b = int(new[i].split(":", 1)[1])
            new[i] = f"bhava:{(b + 5) % 12 + 1}"
        elif kind == "tag_added":
            extra = "phala:death" if section == "phala" else "rel:aspect"
            if extra in new:
                extra = "phala:travel" if section == "phala" else "rel:dignity"
            if extra in new:
                continue
            new.append(extra)
        else:  # tag_dropped
            if len(new) < 2:
                continue
            new.pop(rng.randrange(len(new)))

        if new == tags:
            continue
        out[(section, ref)] = {"kind": kind, "was": tags, "shown": sorted(new)}
    return out


def sensitivity_report(planted_key, got):
    """Did the reviewer catch the deliberately wrong tags? Report BEFORE anything else.

    A reviewer below ~80% here is not reading the Devanagari, and its verdicts on the
    unplanted rows are an opinion rather than a measurement.
    """
    by_kind, caught, seen = defaultdict(lambda: [0, 0]), 0, 0
    missed = []
    for (section, ref), rec in planted_key.items():
        ch, sh = ref.split(".", 1)
        v = got.get((section, ch, sh), (None, ""))[0]
        if v is None:
            continue
        seen += 1
        hit = v in ("wrong", "partial") if rec["kind"] == "tag_dropped" else v == "wrong"
        caught += hit
        by_kind[rec["kind"]][0] += hit
        by_kind[rec["kind"]][1] += 1
        if not hit:
            missed.append((section, ref, rec["kind"], v))
    if not seen:
        return ("  SENSITIVITY: none of the planted rows were reviewed — not measured.\n"
                "  Absent, not a pass.")
    L = ["  === reviewer sensitivity (measured FIRST — the rest means nothing without it)",
         f"    planted rows reviewed: {seen} of {len(planted_key)}",
         f"    CAUGHT: {caught}/{seen} = {100*caught/seen:.0f}%", ""]
    for k, (c, n) in sorted(by_kind.items()):
        L.append(f"      {k:<16}{c}/{n}")
    if missed:
        L += ["", "    missed:"]
        L += [f"      {s}/{r:<10}{k:<16}reviewer said {v!r}" for s, r, k, v in missed[:8]]
    verdict = ("    => USABLE reviewer" if caught / seen >= 0.8 else
               "    => NOT a usable reviewer. Discard its other verdicts.")
    L += ["", verdict]
    return "\n".join(L)


def selftest():
    """The sensitivity measure must be able to report both 0% and 100%.

    rule:discernment-checks §1. Without this the catch rate is a number that cannot fail,
    which is exactly what this whole mechanism exists to stop other people shipping.
    """
    key = {("tags", "1.1"): {"kind": "graha_swapped", "was": [], "shown": []},
           ("tags", "1.2"): {"kind": "chain_reversed", "was": [], "shown": []},
           ("phala", "2.1"): {"kind": "tag_dropped", "was": [], "shown": []}}
    lazy = {("tags", "1", "1"): ("ok", ""), ("tags", "1", "2"): ("ok", ""),
            ("phala", "2", "1"): ("ok", "")}
    keen = {("tags", "1", "1"): ("wrong", ""), ("tags", "1", "2"): ("wrong", ""),
            ("phala", "2", "1"): ("partial", "")}
    lo, hi = sensitivity_report(key, lazy), sensitivity_report(key, keen)
    ok_lo, ok_hi = "CAUGHT: 0/3 = 0%" in lo, "CAUGHT: 3/3 = 100%" in hi
    print(f"  all-`ok` reviewer      -> {'0%   ' if ok_lo else 'NOT 0%'}  {'PASS' if ok_lo else 'FAIL'}")
    print(f"  catches-everything     -> {'100% ' if ok_hi else 'NOT 100%'}  {'PASS' if ok_hi else 'FAIL'}")
    if not (ok_lo and ok_hi):
        print("selftest FAILED: the sensitivity measure cannot report both ends",
              file=sys.stderr)
        return 1
    print("  the sensitivity measure can report both ends")
    return 0


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
    ap.add_argument("--plant", type=int, default=0, metavar="N",
                    help="render N rows with a deliberately wrong tag, to measure whether "
                         "a reviewer is reading the text. The CORPUS is never touched.")
    ap.add_argument("--plant-seed", type=int, default=SEED,
                    help="seed for --plant; the answer key is named after it")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the sensitivity measure can report both 0%% and 100%%")
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

    if args.selftest:
        return selftest()

    if args.score:
        got = read_verdicts(SHEET)
        key_path = PLANT_CACHE / f"plant-{args.plant_seed}.json"
        planted_key = {}
        if key_path.exists():
            planted_key = {tuple(k.split("|", 1)): v
                           for k, v in json.loads(key_path.read_text()).items()}
        if planted_key:
            print(sensitivity_report(planted_key, got))
        else:
            print(f"  no planted-defect key at {key_path} — SENSITIVITY NOT MEASURED.")
            print("  That is not a pass. An unvalidated reviewer's verdicts are an opinion,")
            print("  not a measurement. Regenerate with --plant N before dispatching one.")
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
        # Precision is measured on UNPLANTED rows only. A planted row's `wrong` is the
        # reviewer succeeding, not the tagger failing — counting it as a tag error would
        # make the corpus look worse the harder the reviewer was tested, which is the
        # instrument contaminating the measurement.
        planted_refs = {(s, r.split(".", 1)[0], r.split(".", 1)[1]) for s, r in planted_key}
        for section in ("tags", "phala"):
            sub = {k: v for k, v in got.items()
                   if k[0] == section and k not in planted_refs}
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
            n_planted = sum(1 for k in got if k[0] == section and k in planted_refs)
            print(f"    {n} unplanted rows scored "
                  f"({n_planted} planted rows excluded — they measure the reviewer)")
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

    ph = phala_sample(doc)
    planted = {}
    if args.plant:
        planted = plant(rows, ph, args.plant, args.plant_seed)
        PLANT_CACHE.mkdir(parents=True, exist_ok=True)
        key = PLANT_CACHE / f"plant-{args.plant_seed}.json"
        key.write_text(json.dumps(
            {f"{s}|{r}": v for (s, r), v in planted.items()}, indent=2, ensure_ascii=False))
        # The key lives OUTSIDE the repo on purpose: committed beside the sheet it would
        # be one `grep` from whoever is meant to be reviewing blind.
        print(f"  planted {len(planted)} defect(s) · key -> {key}", file=sys.stderr)

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
        shown = planted.get(("tags", f"{c}.{sh['number']}"), {}).get(
            "shown", sorted(sh.get("tags") or []))
        tags = " ".join(f"`{t}`" for t in shown)
        lines.append(f"| `{c}.{sh['number']}` | {dev} | {tags} | {v} | {note} |")
    lines.append("")

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
            shown = planted.get(("phala", f"{c}.{sh['number']}"), {}).get(
                "shown", sorted(x for x in (sh.get("tags_draft") or [])
                                if x.startswith("phala:")))
            tags = " ".join(f"`{x.split(':', 1)[1]}`" for x in shown) \
                or "*(none — states no result)*"
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
