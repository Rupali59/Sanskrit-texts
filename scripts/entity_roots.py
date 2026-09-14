#!/usr/bin/env python3
"""
Measure the curated entity roots in docs/ENTITY_ROOTS.md against the corpus.

CURATED DOC, GENERATED MEASUREMENT — the split docs/INVENTORY.md has with
check_inventory.py, and docs/RELATION_MARKERS.md with relation_markers.py.
The doc is authoritative for WHICH roots; this file is authoritative for HOW MANY.

The curation cannot be automated and is not attempted here. `ज्ञ` looks like a fine
Mercury root and is 535 tokens of `ज्ञेयं` "should be known"; `तम` looks like a fine
Rahu root and is `सप्तमे` "in the seventh". Only a human reading surface forms rejects
those, which is why the doc's REJECTED table is its longest section.

THREE MEASUREMENTS, and the third is the only real oracle this corpus has produced:

  coverage  verses carrying each entity type
  chains    verses carrying >=2 entities AND a relation — a proposition
  oracle    BPHS ch12-23 treat the twelve bhavas IN ORDER, so ch12+k is the (k+1)th
            house. That number is EXTERNAL to the extraction — nothing about a
            Devanagari compound knows its chapter — so asking whether the most-named
            lord in chapter N is the lord of chapter N's own house is a genuine test.
            Two earlier "100%" oracles in this project were circular; this one is not.

BHAVA IS COUNTED STRICTLY. A bhava name and its phala are the same word — the 2nd house
IS dhana — so `धनं लभते` ("obtains wealth") and `धनेशे` ("the 2nd lord") share a root.
Strict requires a lord-suffix, a locative `-े`, or a position marker. Loose would report
63.3% where strict reports 30.1%, and the loose number is true of bhava VOCABULARY and
false of bhava DISCUSSION.

Exit codes (rule:discernment-checks §2 — absence must be attributable):
  0  ran, measured
  1  the doc's stated coverage disagrees with what was measured
  2  could not run — no doc, no parseable table, or a text_id that does not exist
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "ENTITY_ROOTS.md"

WORD = re.compile(r"[ऀ-ॣ॰-ॿ]+")
TICKED = re.compile(r"`([^`]+)`")
CELLS = re.compile(r"^\|(.+)\|\s*$")

# A bhava root counts only when one of these says a HOUSE is meant, not its phala.
HOUSE_MARK = ("ेश", "ाधिप", "ाधीश", "नाथ", "स्थ", "गत", "भाव", "ांश", "पे")
LORD_SUFFIX = ("ेश", "ाधिप", "ाधीश", "नाथ", "ेश्वर")

# ch12+k is the (k+1)th house. Names per house, for the oracle only.
HOUSE_OF = {"लग्न": 1, "धन": 2, "सहज": 3, "भ्रातृ": 3, "सुख": 4, "वाहन": 4, "मातृ": 4,
            "सुत": 5, "पुत्र": 5, "पञ्चम": 5, "षष्ठ": 6, "रिपु": 6, "अरि": 6, "दार": 7,
            "द्यून": 7, "जाया": 7, "सप्तम": 7, "रन्ध्र": 8, "अष्टम": 8, "भाग्य": 9,
            "धर्म": 9, "पितृ": 9, "कर्म": 10, "राज्य": 10, "लाभ": 11, "व्यय": 12}


def parse_doc(path):
    """Return (roots {type: [root]}, stated {type: verses}, excl {root: [excluded]})."""
    if not path.exists():
        print(f"could not run: no entity doc at {path}", file=sys.stderr)
        return None, None, None
    roots, stated, excl = {}, {}, {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = CELLS.match(line.strip())
        if not m:
            continue
        cells = [c.strip() for c in m.group(1).split("|")]
        if len(cells) < 2:
            continue
        head, second = cells[0], cells[1]
        # exclusion row: both of the first two cells are backticked
        if head.startswith("`") and second.startswith("`"):
            excl.setdefault(TICKED.findall(head)[0], []).extend(TICKED.findall(second))
            continue
        name = head.strip("*").split("·")[0].strip()
        if not re.fullmatch(r"[A-Z_]+|any entity", name):
            continue
        if TICKED.search(second):                      # roots row
            roots.setdefault(name, []).extend(TICKED.findall(second))
        else:                                          # coverage row
            n = re.sub(r"[^\d]", "", second)
            if n:
                stated[name] = int(n)
    if not roots:
        print(f"could not run: parsed {path} but found no root rows", file=sys.stderr)
        return None, None, None
    return roots, stated, excl


def carries(word, root, excl):
    return root in word and not any(e in word for e in excl.get(root, ()))


def bhava_house_sense(word, root):
    """The root is used as a HOUSE here, not as its phala."""
    i = word.find(root) + len(root)
    return (i < len(word) and word[i] == "े") or any(m in word[i - 1:] for m in HOUSE_MARK)


def hit(verse, root, excl, strict):
    words = WORD.findall(verse)
    if strict:
        return any(carries(w, root, excl) and bhava_house_sense(w, root) for w in words)
    return any(carries(w, root, excl) for w in words)


def load_text(text_id):
    for p in sorted(REPO.rglob("*.json")):
        rel = p.relative_to(REPO)
        if rel.parts[0] in ("docs", ".git") or rel.parts[0].startswith("."):
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if doc.get("text_id") == text_id:
            return doc, rel
    return None, None


def run_oracle(doc, roots, excl):
    """Is the most-named lord in ch N the lord of ch N's own house? Returns (raw, adj, total)."""
    raw = adj = total = 0
    bh = roots.get("BHAVA", [])
    for ch in doc.get("chapters") or []:
        n = ch.get("number")
        if not isinstance(n, int) or not 12 <= n <= 23:
            continue
        want = n - 11
        cnt = Counter()
        for sh in ch.get("shlokas") or []:
            for w in WORD.findall(sh.get("text", "")):
                for b in bh:
                    if not carries(w, b, excl) or b not in HOUSE_OF:
                        continue
                    if any(l in w[w.find(b) + len(b) - 1:] for l in LORD_SUFFIX):
                        cnt[HOUSE_OF[b]] += 1
                        break
        if not cnt:
            continue
        total += 1
        raw += cnt.most_common(1)[0][0] == want
        # the lagna-lord is the reference every chapter measures from. POST-HOC rule,
        # added after seeing ch17 and ch19 miss; declared as post-hoc in the doc.
        if want != 1:
            cnt.pop(1, None)
        if cnt:
            adj += cnt.most_common(1)[0][0] == want
    return raw, adj, total


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--text", default="bphs")
    ap.add_argument("--roots", action="store_true",
                    help="print every root one per line (for term_ledger.py --known) and exit")
    args = ap.parse_args()

    roots, stated, excl = parse_doc(DOC)
    if roots is None:
        return 2
    roots.pop("any entity", None)

    if args.roots:
        for r in sorted({r for rs in roots.values() for r in rs}):
            print(r)
        return 0

    doc, rel = load_text(args.text)
    if doc is None:
        print(f"could not run: no text with text_id '{args.text}' under {REPO}", file=sys.stderr)
        return 2
    verses = [s.get("text", "") for c in doc.get("chapters") or []
              for s in c.get("shlokas") or []]
    if not verses:
        print(f"could not run: parsed '{args.text}' but it holds no verses", file=sys.stderr)
        return 2

    tot = len(verses)
    print(f"{args.text}  ({rel})  {tot:,} verses")
    print()
    drift, counts = [], {}
    for name, rs in roots.items():
        strict = name == "BHAVA"
        n = sum(1 for t in verses if any(hit(t, r, excl, strict) for r in rs))
        counts[name] = n
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        flag = ""
        if args.text == "bphs" and stated.get(name) not in (None, n):
            flag = f"   <- doc says {stated[name]:,}"
            drift.append(name)
        star = " (strict)" if name == "BHAVA" else ""
        print(f"  {name:<12}{n:>6,}{100*n/tot:>7.1f}%{star}{flag}")

    any_n = sum(1 for t in verses
                if any(hit(t, r, excl, name == "BHAVA") for name, rs in roots.items() for r in rs))
    print(f"\n  {'ANY':<12}{any_n:>6,}{100*any_n/tot:>7.1f}%")
    if args.text == "bphs" and stated.get("any entity") not in (None, any_n):
        print(f"\ndoc states {stated['any entity']:,} for 'any entity'; measured {any_n:,}",
              file=sys.stderr)
        drift.append("any entity")

    raw, adj, n_ch = run_oracle(doc, roots, excl)
    if n_ch:
        print(f"\n  ORACLE — most-named lord == the chapter's own house, ch12-23")
        print(f"    raw                          {raw}/{n_ch}")
        print(f"    minus the lagna-lord (post-hoc) {adj}/{n_ch}")
        print(f"    the chapter number is EXTERNAL to the extraction, so this is not circular")

    if drift:
        print(f"\nDRIFT: {', '.join(drift)} — update docs/ENTITY_ROOTS.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
