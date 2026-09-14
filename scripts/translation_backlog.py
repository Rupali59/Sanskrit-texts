#!/usr/bin/env python3
"""
Derive the translation backlog per text.

`docs/TRANSLATION_BACKLOG.md` names this script instead of restating its numbers, per
rule:state-and-decisions — a count in a doc rots faster than anything else in it.

Three DIFFERENT jobs are reported separately, because handing them out as one produces
wrong work:

  UNTR   untranslated — `english` is empty. Translate it.
  DRAFT  a machine draft sits in `english_draft`. VERIFY and promote; never copy across unread.
  STUB   `status: translated` but `english` is a generated template, not a translation.
         RE-translate. The worker is replacing text, not filling a blank.

Exit codes are distinguishable on purpose (rule:discernment-checks §2):
  0  ran, reported
  2  could not run — no corpus found, or nothing parsed. NOT a clean backlog.

Run from the repo root: it resolves the corpus relative to the script, not the cwd, because
check_inventory.py's cwd-relative resolution has already produced a "could not run" that read
as broken tooling.
"""

import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# A generated stub, not a translation: "Chapter 21, Shloka 11 - Description of ..."
STUB_RE = re.compile(r"^Chapter \d+, Shloka \d+ *[-–]")


def scan():
    rows, parsed = [], 0
    for p in sorted(REPO.rglob("*.json")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in ("docs", ".git") or rel.parts[0].startswith("."):
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"could not parse {rel}: {e}", file=sys.stderr)
            continue
        tid = j.get("text_id")
        if not tid:
            continue
        parsed += 1
        c, stub = collections.Counter(), 0
        for ch in j.get("chapters") or []:
            for s in ch.get("shlokas") or []:
                st = s.get("status", "untranslated")
                c[st] += 1
                if st == "translated" and STUB_RE.match(s.get("english") or ""):
                    stub += 1
        rows.append({
            "text_id": tid,
            "category": j.get("category", "?"),
            "authority": (j.get("structure") or {}).get("count_authority", ""),
            "total": sum(c.values()),
            "translated": c["translated"],
            "untranslated": c["untranslated"],
            "partial": c["partial"],
            "drafted": c["drafted"],
            "stub": stub,
        })
    return rows, parsed


def main():
    rows, parsed = scan()
    if parsed == 0:
        print(f"could not run: no text_id-bearing JSON found under {REPO}", file=sys.stderr)
        return 2

    rows.sort(key=lambda r: (r["untranslated"] + r["partial"] + r["stub"], r["drafted"]), reverse=True)
    outstanding = [r for r in rows if r["untranslated"] or r["partial"] or r["stub"] or r["drafted"]]

    hdr = f'{"text_id":<30}{"category":<22}{"total":>8}{"UNTR":>8}{"part":>6}{"DRAFT":>7}{"STUB":>6}  authority'
    print(hdr)
    print("-" * len(hdr))
    for r in outstanding:
        print(f'{r["text_id"]:<30}{r["category"]:<22}{r["total"]:>8,}{r["untranslated"]:>8,}'
              f'{r["partial"]:>6}{r["drafted"]:>7,}{r["stub"]:>6}  {r["authority"]}')
    print("-" * len(hdr))

    tot = lambda k: sum(r[k] for r in rows)
    print(f'{parsed} texts scanned · {len(outstanding)} need work · '
          f'{len(rows) - len(outstanding)} complete')
    print(f'TRANSLATE {tot("untranslated") + tot("partial"):,} · '
          f'VERIFY-DRAFT {tot("drafted"):,} · RE-TRANSLATE-STUB {tot("stub"):,} '
          f'(of {tot("total"):,} total)')

    by_cat = collections.Counter()
    for r in rows:
        by_cat[r["category"]] += r["untranslated"] + r["partial"]
    print("\nuntranslated by category:")
    for cat, n in by_cat.most_common():
        if n:
            print(f"  {cat:<24}{n:>8,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
