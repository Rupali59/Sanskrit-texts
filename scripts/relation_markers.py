#!/usr/bin/env python3
"""
Measure the curated relational markers in docs/RELATION_MARKERS.md against the corpus.

WHY A SEPARATE FILE FROM THE MARKERS. The markers are CURATED — three of the first
sixty were rejected only because a human looked at what they matched in the surface
string (`प्` matched `विप्र` "brahmin" 81 times and essentially no lordship). A script
cannot make that call, so it does not try: it reads the table and reports.

Same split as docs/INVENTORY.md <-> check_inventory.py, and docs/TERM_LEDGER.md's
generated-vs-curated columns.

WHAT `--roots` IS FOR. It prints the marker strings one per line, to feed
`term_ledger.py --known`. Recognised relations then drop out of the unknown queue, so
what remains in the ledger is genuinely unrecognised. That is the loop Rupali asked
for: the ledger records what the tagger did not know, and curating it here shrinks the
queue.

Exit codes (rule:discernment-checks §2 — absence must be attributable):
  0  ran, measured
  1  the doc's stated coverage disagrees with what was measured
  2  could not run — no doc, no parseable table, or a text_id that does not exist
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DOC = REPO / "docs" / "RELATION_MARKERS.md"

# A coverage row: | CONCEPT | 1342 | 34.1% | `स्थित` `स्थ` ... |
ROW = re.compile(r"^\|\s*(?:\*\*)?([A-Z_]+|any marker)(?:\*\*)?\s*\|")
TICKED = re.compile(r"`([^`]+)`")
# An exclusion row: | `ेश` | `देश` `क्लेश` | why |   — lowercase/Devanagari first cell, so it
# cannot collide with ROW, which anchors on an ASCII-uppercase concept name.
EXCL_ROW = re.compile(r"^\|\s*`([^`]+)`\s*\|\s*((?:`[^`]+`\s*)+)\|")
WORD = re.compile(r"[ऀ-ॣ॰-ॿ]+")


def blocked(word, marker, excl):
    """True if an exclusion fires on this token.

    A plain exclusion is a SUBSTRING test; one written `=form` is an EXACT-TOKEN test.
    The distinction is not decoration. Excluding `गे` (position, "gone to") from
    stem-final-ग words by substring kills `लग्नगे` and `धनगे` too, because `लग्नगे`
    contains `नग` and `भाग्यगे` contains `भाग` — the exclusion over-matches exactly the
    way the marker it is correcting did. Anchored exclusions say `=योगे`, `=तुङ्गे`,
    `=मृगे` and touch nothing else.
    """
    for e in excl.get(marker, ()):
        if e.startswith("="):
            if word == e[1:]:
                return True
        elif e in word:
            return True
    return False


def matches(verse, marker, excl):
    """True if some TOKEN carries the marker and none of its exclusions.

    Per-token, never per-verse. A verse reading "the lagna-lord causes travel to a
    foreign country" holds both लग्नेशे and विदेशगमनं; it is a true LORDSHIP hit.
    Excluding the whole verse would trade a false positive for a false negative and
    report the trade as an improvement.
    """
    if not excl.get(marker):
        return marker in verse
    return any(marker in w and not blocked(w, marker, excl) for w in WORD.findall(verse))


def load_markers(doc_path):
    """Parse the curated tables. Returns ({concept: [markers]}, {concept: verses}, {marker: [excl]})."""
    if not doc_path.exists():
        print(f"could not run: no marker doc at {doc_path}", file=sys.stderr)
        return None, None, None
    concepts, stated, excl = {}, {}, {}
    for line in doc_path.read_text(encoding="utf-8").splitlines():
        e = EXCL_ROW.match(line)
        if e and not ROW.match(line):
            excl[e.group(1)] = TICKED.findall(e.group(2))
            continue
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        name = m.group(1)
        markers = TICKED.findall(cells[3])
        if not markers:
            continue
        n = re.sub(r"[^\d]", "", cells[1])
        if name == "any marker":
            stated["__any__"] = int(n) if n else None
            continue
        concepts[name] = markers
        stated[name] = int(n) if n else None
    if not concepts:
        print(f"could not run: parsed {doc_path} but found no marker rows", file=sys.stderr)
        return None, None, None
    return concepts, stated, excl


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


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--text", default="bphs", help="text_id to measure (default: bphs)")
    ap.add_argument("--roots", action="store_true",
                    help="print marker strings one per line (for term_ledger.py --known) and exit")
    args = ap.parse_args()

    concepts, stated, excl = load_markers(DOC)
    if concepts is None:
        return 2

    if args.roots:
        for m in sorted({m for ms in concepts.values() for m in ms}):
            print(m)
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
    all_markers = [m for ms in concepts.values() for m in ms]
    any_cov = sum(1 for t in verses if any(matches(t, m, excl) for m in all_markers))

    print(f"{args.text}  ({rel})  {tot:,} verses · {len(all_markers)} markers")
    print()
    drift = []
    for concept, ms in sorted(concepts.items(), key=lambda kv: -sum(
            1 for t in verses if any(matches(t, m, excl) for m in kv[1]))):
        n = sum(1 for t in verses if any(matches(t, m, excl) for m in ms))
        flag = ""
        if args.text == "bphs" and stated.get(concept) not in (None, n):
            flag = f"   <- doc says {stated[concept]:,}"
            drift.append(concept)
        print(f"  {concept:<13}{n:>6,}{100*n/tot:>7.1f}%{flag}")
    print()
    print(f"  {'ANY':<13}{any_cov:>6,}{100*any_cov/tot:>7.1f}%")

    if args.text == "bphs" and stated.get("__any__") not in (None, any_cov):
        print(f"\ndoc states {stated['__any__']:,} for 'any marker'; measured {any_cov:,}",
              file=sys.stderr)
        drift.append("any marker")

    if drift:
        print(f"\nDRIFT: {', '.join(drift)} — update docs/RELATION_MARKERS.md", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
