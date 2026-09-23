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

Two sources, one default
-------------------------
The corpus-summarising half of this script now lives in `sanskrit_texts.reader` -- the first
real consumer of the modelled store (plan §5). `--source json` (the default, unchanged
behaviour) walks the files exactly as before. `--source db` reads the same summary shape
through the published API surface instead, and compares it against the json source rather
than against INVENTORY.md: the two are not expected to agree field-for-field (see
`reader.py`'s module docstring for which fields the db source cannot see, and why), only on
which texts exist and how many verses each holds.

**This script still runs under bare system `python3`, with no dependencies, for the default
json source.** `sanskrit_texts.reader` imports `sqlalchemy` only lazily, inside the db-source
function, so importing the package here costs nothing extra on the path this script's own
runbook position depends on (docs/DATABASE.md: this check gates the importer, so it must be
runnable before anything is installed). `--source db` DOES need the project's dependencies
(`sqlalchemy`, a live database) and is expected to be run under `.venv-corpus/bin/python`.

Run:  python3 scripts/check_inventory.py [--path .] [--source json|db]
Exit: 0 = matches, 1 = drift, 2 = could not run.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
from pathlib import Path

# The package lives at the repo root, one level above this script -- and `python3
# scripts/check_inventory.py` puts only `scripts/` on sys.path, not the root. Without this,
# `import sanskrit_texts` fails under exactly the invocation the module docstring above
# promises still works.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from sanskrit_texts.reader import load_corpus_from_db, load_corpus_from_json  # noqa: E402

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


# `load_corpus` used to live here. It is now `sanskrit_texts.reader.load_corpus_from_json`,
# moved unchanged (not rewritten) so `--source json` -- the default -- behaves identically to
# before the move; verified by diffing this script's output pre- and post-migration.


def check_db_vs_json(root: Path, quiet: bool) -> int:
    """`--source db`: compare the store, through the published API surface, against the json
    source -- NOT against INVENTORY.md. The two sources cannot agree field-for-field (see
    `reader.py`'s module docstring); what both can see in full is which texts exist and how
    many verses each holds, so that is what this asserts.
    """
    try:
        db = load_corpus_from_db()
    except RuntimeError as e:
        print(f"could not run: {e}", file=sys.stderr)
        return 2
    except ModuleNotFoundError as e:
        # The json path (the default) stays dependency-free on purpose (module docstring).
        # --source db is not, and a bare `python3` traceback here would read as this SCRIPT
        # being broken rather than as "wrong interpreter" -- say which interpreter it needs.
        print(
            f"could not run: {e}. --source db needs this project's dependencies -- run under "
            f".venv-corpus/bin/python, e.g. `make check` or "
            f"`.venv-corpus/bin/python {Path(__file__).name} --source db`.",
            file=sys.stderr,
        )
        return 2

    json_corpus = load_corpus_from_json(root)

    try:
        from sanskrit_texts.exclusions import EXCLUDED_TEXTS
    except ImportError:
        EXCLUDED_TEXTS = {}

    fail: list[str] = []

    db_ids, json_ids = set(db), set(json_corpus)
    expected_absent = set(EXCLUDED_TEXTS) & json_ids
    missing = json_ids - db_ids
    unexplained_missing = missing - expected_absent
    extra = db_ids - json_ids
    # D11 (DECISIONS.md 2026-09-16): the importer creates ONE verse-less parent row per
    # multi-part work (siddhanta_shiromani today) from the directory name -- it has no source
    # file, so it can never appear in the json corpus by construction. Detected structurally
    # (0 verses, present only in the db) rather than by name, so a second such text needs no
    # change here -- a hardcoded single-name list is exactly G17's failure mode.
    synthetic_parents = {t for t in extra if db[t]["sh"] == 0}
    unexplained_extra = extra - synthetic_parents

    fail += [
        f"{t}: in the database, names no text in the json corpus, and carries {db[t]['sh']} "
        f"verses -- not the verse-less parent-of-parts shape D11 predicts"
        for t in sorted(unexplained_extra)
    ]
    fail += [
        f"{t}: in the json corpus, absent from the database, and NOT in exclusions.py"
        for t in sorted(unexplained_missing)
    ]

    for tid in sorted(db_ids & json_ids):
        d, j = db[tid], json_corpus[tid]
        # The importer REFUSES duplicate (section, label) pairs unless run with
        # --allow-partial (STATE.md 2026-09-16: the current store was). Those verses are
        # never stored, so a shloka-count gap up to `dupes` is the documented, accepted loss
        # -- not drift. Anything beyond that IS drift.
        allowed_gap = j["dupes"] or 0
        gap = j["sh"] - d["sh"]
        if gap < 0 or gap > allowed_gap:
            fail.append(
                f"{tid}: json has {j['sh']} shlokas, db has {d['sh']} "
                f"(gap {gap}, accounted for by at most {allowed_gap} refused duplicates)"
            )

    if not quiet:
        print(f"db: {len(db_ids)} texts · json: {len(json_ids)} texts")
        if expected_absent:
            print(
                f"{len(expected_absent)} excluded by decision (sanskrit_texts/exclusions.py, "
                f"GOTCHAS G62), correctly absent from the db: {', '.join(sorted(expected_absent))}"
            )
        if synthetic_parents:
            print(
                f"{len(synthetic_parents)} verse-less parent-of-parts (D11), correctly absent "
                f"from the json corpus: {', '.join(sorted(synthetic_parents))}"
            )
        print(
            f"{sum(d['sh'] for d in db.values()):,} shlokas in the db · "
            f"{sum(j['sh'] for j in json_corpus.values()):,} in the json source"
        )

    if fail:
        print(f"\nDRIFT — {len(fail)} finding(s):", file=sys.stderr)
        for f in fail:
            print(f"  {f}", file=sys.stderr)
        return 1
    if not quiet:
        print("db agrees with the json source on text count and shloka count")
    return 0


def _colophon_chapters(root: Path) -> list:
    """SC-001 candidates across the corpus. Stdlib only, so `--source json` stays dependency-free."""
    from sanskrit_texts.structure_checks import colophon_only_chapters
    out = []
    for path in sorted(root.rglob("*.json")):
        rel = path.relative_to(root)
        if rel.parts[0] == "docs" or any(part.startswith(".") for part in rel.parts):
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(doc, dict) and "text_id" in doc and "chapters" in doc:
            out.extend(colophon_only_chapters(doc))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", default=".", help="corpus root (default: cwd)")
    ap.add_argument("--quiet", action="store_true", help="print only failures")
    ap.add_argument(
        "--source",
        choices=("json", "db"),
        default="json",
        help="json (default): walk the corpus files, as always. "
        "db: read the store through the published API surface and compare it against "
        "json instead of INVENTORY.md (see reader.py for why).",
    )
    args = ap.parse_args()

    root = Path(args.path).resolve()

    if args.source == "db":
        return check_db_vs_json(root, args.quiet)

    inv_path = root / "docs" / "INVENTORY.md"
    if not inv_path.is_file():
        print(f"could not run: no {inv_path}", file=sys.stderr)
        return 2

    corpus = load_corpus_from_json(root)
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
        # SC-001, reported not gated — same posture as the dedupe-loss line above. These are
        # real defects in committed data, so hiding them would be wrong; but they are not
        # registry drift, and failing the gate on them would make `make check` red until a
        # human has read the texts against an edition. Derive, never restate: this printed
        # 2 on 2026-09-23 (kaushitaki_upanishad, kaivalya_upanishad).
        orphans = _colophon_chapters(root)
        if orphans:
            certain = [o for o in orphans if o.ordinal_is_lower]
            print(
                f"{len(orphans)} colophon-only chapter(s) — SC-001, a chapter boundary drawn "
                f"AT the colophon instead of after it"
                + (f"; {len(certain)} certain (the colophon closes a LOWER-numbered division)"
                   if certain else "")
            )
            for o in orphans:
                print(f"  {o}")

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
