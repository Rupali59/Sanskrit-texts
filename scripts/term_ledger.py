#!/usr/bin/env python3
"""
Unknown-term ledger — what the tagger met and did not recognise.

WHY THIS EXISTS. Statistical vocabulary induction over this corpus was measured and
rejected (docs/EMBEDDING_EVAL.md and the adversarial review of 2026-09-14): it
recovered 12 stems with 91 false positives, and — fatally — it omitted 4 of Mars's
6 roots with every guard reporting green, because absence of a form is
indistinguishable from absence of evidence.

This is the loud version of the same discovery goal. A tagger's ERRORS are visible
in the surface string. Its OMISSIONS are not, unless something records them. An
unknown term with 200 occurrences is obviously worth a human's attention; a synonym
missing from an induced ring is invisible forever.

TWO PARTS, the pattern this repo already uses (docs/INVENTORY.md <-> check_inventory.py):
  * counts, distributions and examples are GENERATED and never hand-maintained
  * dispositions are CURATED and survive regeneration

TRIAGE, NOT EXTRACTION. The `signal` column ranks what a human looks at first. It
makes no claim. Keyness measures against Sanskrit are documented to surface register
markers (iti, proktam, bhavet) as confident false positives, so this orders a review
queue and never decides anything.

NO IMPORTED STOPWORD LIST. BPHS's type/token ratio is 0.49 — sandhi makes nearly
every word unique, so frequency is a weak signal. Only genuine function words are
pre-listed; `common` is a verdict a human records, not a list we assume.

Exit codes (rule:discernment-checks §2 — absence must be attributable):
  0  ran, ledger written
  2  could not run — no corpus, nothing parsed, or a text_id that does not exist
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LEDGER = REPO / "docs" / "TERM_LEDGER.md"

# Devanagari LETTERS and matras only. The block ऀ-ॿ also contains the dandas
# । ॥ (U+0964-5) and the digits ०-९ (U+0966-F) — punctuation and numerals, not
# words. Without this exclusion `।` tops the ledger at 3,924 occurrences, which is
# a measurement of the verse separator. (G17 is the same hazard in the other
# direction: Python's \d MATCHES Devanagari digits, so use explicit ranges.)
DEVANAGARI = re.compile(r"[ऀ-ॣ॰-ॿ]+")

# Genuine function words only. Everything else earns its disposition by review.
FUNCTION_WORDS = {
    "च", "वा", "तु", "हि", "यदि", "तदा", "एव", "अपि", "न", "तत्", "स", "सा",
    "इति", "अथ", "यत्", "यः", "ये", "ते", "तेषां", "तस्य", "तथा", "किं", "अत्र",
}

# A term in <= this many chapters reads as a TOPIC term; >= SPREAD_FRAC of all
# chapters reads as function vocabulary. Both are triage hints, not verdicts.
TOPIC_MAX_CHAPTERS = 3
SPREAD_FRAC = 0.20

DISPOSITIONS = {"unreviewed", "entity", "relation", "common", "noise"}


def load_text(text_id):
    """Return (doc, path) for a text_id, or (None, None)."""
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


def load_known(paths):
    """Root list(s) the tagger recognises. Absent file is not an error — it means
    nothing is known yet, which is the correct state before step 1."""
    known = set()
    for p in paths:
        f = Path(p)
        if not f.is_absolute():
            f = REPO / f
        if not f.exists():
            print(f"note: no root list at {f} — every term will be unreviewed", file=sys.stderr)
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if line:
                known.add(line)
    return known


def parse_ledger(path):
    """Read curated dispositions out of an existing ledger. Generated columns are
    discarded — they are regenerated. Returns {term: (disposition, resolved_to)}."""
    if not path.exists():
        return {}
    curated = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 7:
            continue
        term = cells[0].strip("`")
        disp = cells[5]
        resolved = cells[6]
        if disp in DISPOSITIONS:
            curated[term] = (disp, resolved)
    return curated


def scan(doc, known):
    """Return per-term counts, chapter distribution and example refs."""
    count = Counter()
    chapters = defaultdict(set)
    examples = defaultdict(list)
    n_chapters = 0

    for ch in doc.get("chapters") or []:
        n_chapters += 1
        cn = ch["number"]
        for sh in ch.get("shlokas") or []:
            seen = set()
            for tok in DEVANAGARI.findall(sh.get("text", "")):
                if tok in FUNCTION_WORDS:
                    continue
                if any(k in tok for k in known):
                    continue  # the tagger recognised it
                seen.add(tok)
            for tok in seen:
                count[tok] += 1
                chapters[tok].add(cn)
                if len(examples[tok]) < 3:
                    examples[tok].append(f"{cn}.{sh['number']}")
    return count, chapters, examples, n_chapters


def signal_for(n_ch, n_total):
    if n_ch <= TOPIC_MAX_CHAPTERS:
        return "TOPIC"
    if n_ch >= max(2, int(n_total * SPREAD_FRAC)):
        return "SPREAD"
    return "MIXED"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--text", default="bphs", help="text_id to scan (default: bphs)")
    ap.add_argument("--known", action="append", default=[],
                    help="file of recognised roots, one per line (repeatable)")
    ap.add_argument("--min-count", type=int, default=2,
                    help="omit terms below this verse count (default 2)")
    ap.add_argument("--limit", type=int, default=400, help="rows to write (default 400)")
    ap.add_argument("--out", default=str(LEDGER))
    args = ap.parse_args()

    doc, rel = load_text(args.text)
    if doc is None:
        print(f"could not run: no text with text_id '{args.text}' under {REPO}", file=sys.stderr)
        return 2

    known = load_known(args.known)
    count, chapters, examples, n_chapters = scan(doc, known)
    if not count:
        print(f"could not run: parsed '{args.text}' but found no Devanagari tokens", file=sys.stderr)
        return 2

    out = Path(args.out)
    curated = parse_ledger(out)

    rows = [t for t, n in count.items() if n >= args.min_count]
    rows.sort(key=lambda t: (-count[t], t))
    shown = rows[: args.limit]

    disp_counts = Counter(curated.get(t, ("unreviewed", ""))[0] for t in rows)
    # Only a NON-`unreviewed` disposition represents a human decision. Counting
    # carried-forward `unreviewed` rows would report "399 curated" on a ledger where
    # nobody has decided anything — a number that reads as work done.
    carried = sum(1 for t in rows if curated.get(t, ("unreviewed", ""))[0] != "unreviewed")

    lines = [
        "# Term ledger — what the tagger did not recognise",
        "",
        "**Generated by `scripts/term_ledger.py`. Do not hand-edit the generated columns —",
        "they are overwritten on every run. `disposition` and `resolved_to` ARE curated and",
        "are carried across regenerations; that split is the same one `docs/INVENTORY.md` has",
        "with `check_inventory.py`.**",
        "",
        "Why this file exists: a tagger's *errors* are visible in the surface string, but its",
        "*omissions* are not. Statistical induction over this corpus omitted 4 of Mars's 6",
        "roots with every check reporting green. This records what was not recognised so an",
        "omission is something a human can see.",
        "",
        "`signal` is a **triage hint that ranks review order and makes no claim** — `TOPIC` =",
        f"appears in ≤{TOPIC_MAX_CHAPTERS} chapters (likely subject vocabulary), `SPREAD` =",
        f"appears in ≥{int(SPREAD_FRAC*100)}% of chapters (likely function vocabulary).",
        "Keyness measures against Sanskrit are documented to surface register markers as",
        "confident false positives, so this never decides a disposition.",
        "",
        f"Regenerate: `python3 scripts/term_ledger.py --text {args.text}"
        + "".join(f" --known {k}" for k in args.known) + "`",
        "",
        "## Run",
        "",
        f"- text: `{args.text}` ({rel})",
        f"- chapters scanned: {n_chapters}",
        f"- recognised roots loaded: {len(known)}",
        f"- distinct unrecognised terms (count ≥ {args.min_count}): **{len(rows):,}**",
        f"- rows written: {len(shown):,} of {len(rows):,}",
        f"- curated dispositions carried forward: **{carried}**",
        f"- disposition tally: "
        + " · ".join(f"{k} {v}" for k, v in sorted(disp_counts.items())),
        "",
        "## Terms",
        "",
        "| term | verses | chapters | signal | examples | disposition | resolved_to |",
        "|---|---:|---:|---|---|---|---|",
    ]
    for t in shown:
        disp, resolved = curated.get(t, ("unreviewed", ""))
        n_ch = len(chapters[t])
        lines.append(
            f"| `{t}` | {count[t]} | {n_ch} | {signal_for(n_ch, n_chapters)} "
            f"| {', '.join(examples[t])} | {disp} | {resolved} |"
        )
    lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"{args.text}: {len(rows):,} unrecognised terms (count >= {args.min_count}), "
          f"{len(shown):,} written, {carried} curated dispositions carried")
    print(f"-> {out.relative_to(REPO) if out.is_relative_to(REPO) else out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
