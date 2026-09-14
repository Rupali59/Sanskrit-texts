#!/usr/bin/env python3
"""Reconcile docs/INVENTORY.md against the corpus it claims to describe.

Why this exists
---------------
INVENTORY.md is the `text_id` registry and it is hand-maintained. On 2026-09-14 every one
of its 66 per-text rows was correct while the **Totals line above them** said 54 texts /
918 chapters / 92,166 shlokas against a true 66 / 955 / 97,794 — and a second summary table
twelve lines further down disagreed with both. The rows were maintained; the aggregates were
not, and nothing could tell the difference.

`rule:state-and-decisions`: a count in a state file rots faster than anything else in it.
This script is the "name the command that derives the number" half of that rule.

What it asserts
---------------
1. Every corpus text has exactly one registry row, and every row names a real text.
2. Each row's chapters / shlokas / translated% / directory match the JSON.
3. The Totals line matches the sum.
4. In the acquisition table, `HELD` rows have a text_id in the corpus and non-HELD rows
   do not. That is the check the old ✅-prefix-plus-two-banners layout could not support.

It reports "looked at nothing" differently from "found nothing" (`rule:discernment-checks`
§2 and §6): if a table parses to zero rows the script fails rather than passing quietly.

Run:  python3 scripts/check_inventory.py [--path .]
Exit: 0 = registry matches the corpus, 1 = drift, 2 = could not run.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

REGISTRY_ROW = re.compile(
    r"^\|\s*`(?P<tid>[a-z0-9_]+)`\s*\|\s*\[`(?P<dir>[^`]+)`\][^|]*\|"
    r"\s*(?P<ch>[\d,]+)\s*\|\s*(?P<sh>[\d,]+)\s*\|\s*(?P<pct>[^|]*?)\s*\|"
)
TOTALS = re.compile(
    r"\*\*Totals:\s*(?P<texts>[\d,]+) texts\s*·\s*(?P<ch>[\d,]+) chapters\s*·\s*"
    r"(?P<sh>[\d,]+) shlokas\s*·\s*(?P<cat>\d+) categories\*\*"
)
# Acquisition table: | `<name>` | `<STATUS>` | ... — status is the second cell, backticked.
ACQ_ROW = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*`?(?P<status>[A-Z]{4,10})`?\s*\|(?P<rest>.*)$"
)
ACQ_HEADING = "## Acquisition status"
TICKED = re.compile(r"`([a-z0-9_]+)`")
ACQ_STATUSES = {"HELD", "SOURCED", "REFUSED", "UNSOURCED", "LOST"}

_int = lambda s: int(s.replace(",", ""))
# Squash to letters+digits so "Siddhanta Shiromani" in a title matches a "SiddhantaShiromani" row.
_squash = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())


def load_corpus(root: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for p in sorted(root.rglob("*.json")):
        rel = p.relative_to(root)
        # `docs/` is prose; a dot-directory is tooling config (.claude/, .cursor/) and an
        # unparseable settings.json there must not read as a corpus failure.
        if rel.parts[0] == "docs" or any(part.startswith(".") for part in rel.parts):
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise SystemExit(f"could not run: {rel} is not readable JSON ({e})")
        tid = j.get("text_id")
        if not tid:
            continue
        chs = j.get("chapters") or []
        n = sum(len(c.get("shlokas", [])) for c in chs)
        # Dedupe loss: astroacharya's seed_texts.py keys on (chapter, shloka), later wins, and
        # only LOGS the collision — so a duplicate key is a shloka that never reaches Mongo
        # (G8). The registry's Shlokas column counts what is present, not what is ingestible.
        keys: collections.Counter = collections.Counter()
        for c in chs:
            for sh in c.get("shlokas", []):
                keys[(c.get("number"), sh.get("number"))] += 1
        dupes = sum(v - 1 for v in keys.values() if v > 1)
        tr = sum(
            1 for c in chs for s in c.get("shlokas", []) if s.get("status") == "translated"
        )
        if tid in out:
            raise SystemExit(f"could not run: text_id {tid!r} declared twice")
        out[tid] = {
            "ch": len(chs),
            "sh": n,
            "tr": tr,
            "pct": round(100 * tr / n) if n else 0,
            "dir": str(rel.parent),
            "cat": j.get("category"),
            "dupes": dupes,
            "titles": f"{j.get('title_en', '')} {j.get('title_sa', '')}",
            "authority": (j.get("structure") or {}).get("count_authority"),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="corpus root (default: cwd)")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    args = ap.parse_args()

    root = Path(args.path).resolve()
    inv_path = root / "docs" / "INVENTORY.md"
    if not inv_path.is_file():
        print(f"could not run: no {inv_path}", file=sys.stderr)
        return 2

    corpus = load_corpus(root)
    if not corpus:
        print(f"could not run: no text_id-bearing JSON under {root}", file=sys.stderr)
        return 2

    text = inv_path.read_text(encoding="utf-8")
    rows: dict[str, dict] = {}
    acq: list[tuple[str, str]] = []
    for line in text.splitlines():
        if m := REGISTRY_ROW.match(line):
            rows[m["tid"]] = {
                "dir": m["dir"].rstrip("/"),
                "ch": _int(m["ch"]),
                "sh": _int(m["sh"]),
                "pct": m["pct"].strip(),
            }
        elif m := ACQ_ROW.match(line):
            if (st := m["status"].strip()) in ACQ_STATUSES:
                acq.append((m["name"].strip().strip("`"), st, m["rest"]))

    # A parser that finds nothing must say so rather than reporting a clean run.
    if not rows:
        print("could not run: parsed 0 registry rows — the table layout changed", file=sys.stderr)
        return 2

    fail: list[str] = []

    missing = sorted(set(corpus) - set(rows))
    orphan = sorted(set(rows) - set(corpus))
    fail += [f"{t}: in the corpus, absent from the registry" for t in missing]
    fail += [f"{t}: registry row names no text in the corpus" for t in orphan]

    for tid in sorted(set(corpus) & set(rows)):
        c, r = corpus[tid], rows[tid]
        if c["ch"] != r["ch"]:
            fail.append(f"{tid}: registry says {r['ch']} chapters, corpus has {c['ch']}")
        if c["sh"] != r["sh"]:
            fail.append(f"{tid}: registry says {r['sh']} shlokas, corpus has {c['sh']}")
        claimed = r["pct"].rstrip("*").rstrip("%")
        if claimed.isdigit() and int(claimed) != c["pct"]:
            fail.append(f"{tid}: registry says {r['pct']} translated, corpus has {c['pct']}%")
        if r["dir"] != c["dir"]:
            fail.append(f"{tid}: registry path {r['dir']!r}, corpus path {c['dir']!r}")

    if m := TOTALS.search(text):
        want = (
            len(corpus),
            sum(v["ch"] for v in corpus.values()),
            sum(v["sh"] for v in corpus.values()),
            len({v["cat"] for v in corpus.values()}),
        )
        got = (_int(m["texts"]), _int(m["ch"]), _int(m["sh"]), int(m["cat"]))
        if want != got:
            fail.append(
                "Totals line says %d texts / %d chapters / %d shlokas / %d categories; "
                "corpus has %d / %d / %d / %d" % (*got, *want)
            )
    else:
        fail.append("no **Totals:** line found — cannot check the aggregate")

    # A text that loses shlokas to the seeder MUST say so. Three texts do (declared
    # 2026-09-14 after a corpus-wide audit found 70 losses across five distinct shapes);
    # any NEW one is a silent regression. This is the check whose absence let 55 shlokas
    # sit un-ingested in jataka_parijata for months: contiguity passed, totals matched,
    # and only key DISTINCTNESS broke — which nothing tested, because seed_texts.py logs
    # the collision and drops the row rather than failing (G8).
    for tid in sorted(corpus):
        v = corpus[tid]
        if v["dupes"] and not v["authority"]:
            fail.append(
                f"{tid}: loses {v['dupes']} shloka(s) to the (chapter, shloka) dedupe but "
                f"declares no count_authority — a silent loss must be declared, not discovered"
            )

    # HELD must mean held. This is what the ✅-prefix-plus-banners layout could not assert.
    # A section that exists but parses to zero rows is a READER FAILURE, not a clean result
    # (`rule:discernment-checks` §2/§6) — this check reported "0 acquisition rows" and passed
    # on its first run, which is the very failure it exists to catch.
    if ACQ_HEADING in text and not acq:
        print(
            f"could not run: found {ACQ_HEADING!r} but parsed 0 status rows — layout changed",
            file=sys.stderr,
        )
        return 2
    for name, status, rest in acq:
        ids = {t for t in TICKED.findall(rest) if t in corpus}
        if status == "HELD" and not ids:
            fail.append(f"acquisition row {name!r}: HELD but names no text_id in the corpus")
        if status != "HELD" and ids:
            fail.append(
                f"acquisition row {name!r}: status {status} but {sorted(ids)} is in the corpus"
            )
        # A row can be held under a DIFFERENT name than its own — Siddhanta Shiromani was
        # digitised as its four parts (lilavati, bijaganita, grahaganita, goladhyaya), each
        # naming the parent work only in `title_en`. The id check above cannot see that, so
        # this one matches the row name against every text's titles. Found 2026-09-14, with
        # the row still saying digitisation was the remaining work.
        if status != "HELD":
            key = _squash(name)
            if key:
                hit = sorted(t for t, v in corpus.items() if key in _squash(v["titles"]))
                if hit:
                    fail.append(
                        f"acquisition row {name!r}: status {status}, but {hit} "
                        f"name it in their title — it may already be held"
                    )
    if not args.quiet:
        loss = sum(v["dupes"] for v in corpus.values())
        worst = sorted(
            ((v["dupes"], t) for t, v in corpus.items() if v["dupes"]), reverse=True
        )
        print(f"{len(corpus)} texts · {len(rows)} registry rows · {len(acq)} acquisition rows")
        print(
            f"{sum(v['sh'] for v in corpus.values()):,} shlokas present · "
            f"{loss} lost to the seeder's (chapter, shloka) dedupe"
            + (f" — {', '.join(f'{t} {n}' for n, t in worst)}" if worst else "")
        )

    if fail:
        print(f"\nDRIFT — {len(fail)} finding(s):", file=sys.stderr)
        for f in fail:
            print(f"  {f}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("registry matches the corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
