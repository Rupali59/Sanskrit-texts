#!/usr/bin/env python3
"""Rank held texts by how likely their `docs/INVENTORY.md` row is lying.

WHY THIS IS NOT `check_inventory.py`, AND WHY BOTH EXIST. That script reconciles the registry's
chapter and shloka COUNTS against the corpus. It is correct and it passes -- it printed "registry
matches the corpus" on 2026-09-29, the same day `mayamata` was found advertised at **100%
translated** while holding **zero** translations: all 3,351 of its `english` values are the
verse's own Devanagari behind a template prefix. Counting rows and checking a field is non-empty
cannot see a text that is the wrong work, a generated template, or the Sanskrit copied into the
translation field. `rule:discernment-checks` 5 -- two green checks that measure the same wrong
thing are not corroboration.

SIX SIGNALS. Each is a defect class this corpus has actually paid for, not a hypothetical:

  skel       distinct Sanskrit SKELETONS / verses. **G62**: collapse digit runs to `N` and count.
             A real 300-verse text has ~300 skeletons; `deva_keralam` had TWO, and every
             numbering and contiguity check passed on it.
  uniq       distinct Sanskrit / verses. A Samhita repeats by design -- `atharvaveda_samhita`
             has 53 legitimately identical groups -- so this is a place to LOOK, never a verdict.
  echo       served value == the verse's own Sanskrit, byte-identical after the template prefix.
             This is exactly how `mayamata` reads, and how 67,820 values read in 2026-09-16.
  noSa       verses with an empty `text`. A translation with no source is its own defect class.
  latin      Latin letters inside the Sanskrit -- apparatus sigla, editors' English notes, OCR
             bleed. **Read the hits before believing them; see the warning below.**
  claim-gap  INVENTORY's percentage minus the measured clean percentage.

THE `latin` SIGNAL HAS A KNOWN, LEGITIMATE TOP SCORER, AND THAT IS THE POINT.
`samaveda_samhita` scores **1.00** -- every verse -- because the Samaveda addresses itself with
arcika references (`0101a`, `0102c`), which are citation components, not contamination. It is the
worst-scoring text in the corpus on that signal and it has no defect at all. **A threshold would
condemn it first.** So this script RANKS and never judges: it tells you where to open a file.

`rule:discernment-checks` 1 -- run `--selftest` first. It builds a corpus whose defects are known
by construction and asserts each signal fires, so a green run here is evidence rather than a
claim. A check that cannot fail is worse than no check.

    ./.venv-corpus/bin/python scripts/check_inventory_suspects.py
    ./.venv-corpus/bin/python scripts/check_inventory_suspects.py --selftest

Exit: 0 nothing scored, 1 suspects found (advisory -- NOT a merge gate; six of the seven it
found on 2026-09-29 were real and the seventh was the Samaveda above), 2 a floor tripped.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
import tempfile
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from sanskrit_texts.importer import corpus_files  # noqa: E402
from sanskrit_texts.translation_status import check_value  # noqa: E402

LATIN = re.compile(r"[A-Za-z]")
#: `[0-9]` and the Devanagari block named explicitly -- NEVER `\d`, which is Unicode-aware and
#: eats Devanagari numerals that are real citation components (**G17**).
NUM = re.compile(r"[0-9०-९]+")
#: text_id | path | chapters | shlokas | percent |
ROW = re.compile(r"^\|\s*`([a-z0-9_]+)`\s*\|.*?\|\s*([\d,]+)\s*\|\s*([\d,]+)\s*\|\s*(\d+)%\s*\|")

#: Floors. "Found nothing" and "looked at nothing" must be different outputs
#: (`rule:discernment-checks` 2). Both are deliberately far below the real figures (66/66).
MIN_TEXTS = 50
MIN_ROWS = 50


def _norm(text: str) -> str:
    return " ".join(unicodedata.normalize("NFC", text or "").split())


def _skeleton(text: str) -> str:
    return NUM.sub("N", _norm(text))


def read_registry(repo: pathlib.Path) -> dict[str, int]:
    """`{text_id: claimed_percent}` from the INVENTORY table."""
    path = repo / "docs" / "INVENTORY.md"
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = ROW.match(line)
        if m:
            out[m.group(1)] = int(m.group(4))
    return out


def measure(repo: pathlib.Path, registry: dict[str, int]) -> list[dict]:
    rows = []
    for path in corpus_files(repo):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "chapters" not in doc:
            continue
        verses = [s for c in doc["chapters"] for s in (c.get("shlokas") or [])]
        if not verses:
            continue
        n = len(verses)
        sanskrit = [_norm(s.get("text") or "") for s in verses]
        present = [t for t in sanskrit if t]

        echo = clean = 0
        for shloka, sa in zip(verses, sanskrit):
            english = (shloka.get("english") or "").strip()
            if not english:
                continue
            body = english.split(": ", 1)[1] if ": " in english else english
            if sa and _norm(body) == sa:
                echo += 1
            if not check_value("en", english, shloka.get("text") or ""):
                clean += 1

        rows.append({
            "id": doc.get("text_id"),
            "n": n,
            "skel": len({_skeleton(t) for t in present}) / n if present else 0.0,
            "uniq": len(set(present)) / n if present else 0.0,
            "echo": echo / n,
            "noSa": (n - len(present)) / n,
            "latin": sum(1 for t in sanskrit if LATIN.search(t)) / n,
            "claimed": registry.get(doc.get("text_id")),
            "actual": round(100 * clean / n),
        })
    return rows


def score(row: dict) -> float:
    """Weighted, and the weights encode what each defect COST, not how odd it looks.

    `echo` and `noSa` are the two that have actually published non-translations, so they
    dominate. `latin` is weighted lowest on purpose -- its top scorer is legitimate.
    """
    total = 0.0
    if row["skel"] < 0.90:
        total += (0.90 - row["skel"]) * 300
    if row["uniq"] < 0.90:
        total += (0.90 - row["uniq"]) * 100
    total += row["echo"] * 200
    total += row["noSa"] * 250
    total += row["latin"] * 60
    if row["claimed"] is not None:
        total += max(0, row["claimed"] - row["actual"]) * 2
    return total


def render(rows: list[dict]) -> int:
    rows = sorted(rows, key=lambda r: -r["score"])
    flagged = [r for r in rows if r["score"] >= 1]
    header = (f"{'text_id':26}{'verses':>8}{'skel':>7}{'uniq':>7}{'echo':>7}"
              f"{'noSa':>7}{'latin':>7}{'claim':>7}{'real':>6}{'score':>8}")
    print(header)
    print("-" * len(header))
    for r in flagged:
        claim = f"{r['claimed']}%" if r["claimed"] is not None else "-"
        print(f"{r['id']:26}{r['n']:8,}{r['skel']:7.2f}{r['uniq']:7.2f}{r['echo']:7.2f}"
              f"{r['noSa']:7.2f}{r['latin']:7.2f}{claim:>7}{str(r['actual']) + '%':>6}"
              f"{r['score']:8.0f}")
    print(f"\n{len(flagged)} flagged, {len(rows) - len(flagged)} raised no signal.")
    print("skel/uniq are DISTINCT-VALUE RATIOS -- 1.00 ideal, low means a template or repetition.")
    print("echo/noSa/latin are FRACTIONS OF VERSES -- 0.00 ideal.")
    print("OPEN EVERY HIT BEFORE BELIEVING IT. `samaveda_samhita` scores latin 1.00 and is CLEAN:")
    print("its arcika references (`0101a`) are citation components. This ranks; it never judges.")
    return 1 if flagged else 0


def _text(text_id: str, verses: list[dict]) -> dict:
    return {"text_id": text_id, "title_sa": "x", "title_en": "x", "category": "test",
            "chapters": [{"number": 1, "title": "x", "shlokas": verses}]}


def selftest() -> int:
    """Build a corpus whose defects are known BY CONSTRUCTION and assert each signal fires."""
    real = "रामो राजमणिः सदा"
    #: Distinct BODIES, never one body with an index appended. The first version of this fixture
    #: built the clean case as f"{real} {i}" and it scored **265** -- because collapsing digit runs
    #: to `N` makes sixty index-suffixed verses ONE skeleton, which is G62's method working exactly
    #: as designed. `rule:mutate-behind-the-fixture-builder`: the fixture decides what the check
    #: can see, and a convenient one had made the honest case indistinguishable from the defect.
    words = ["अग्नि", "इन्द्र", "सोम", "वायु", "सूर्य", "चन्द्र", "मित्र", "वरुण", "रुद्र", "विष्णु"]

    def body(i: int) -> str:
        """A distinct Sanskrit body per verse.

        The two indices must vary INDEPENDENTLY. A first attempt used `i % 10` and
        `(i * 7 + 3) % 10`, and both are functions of `i % 10`, so sixty verses produced ten
        distinct bodies and the clean case still scored 293. `i % n` with `i // n` is unique
        for every i below n squared, which is the property actually wanted.
        """
        return f"{words[i % len(words)]} {words[(i // len(words)) % len(words)]} {real}"

    with tempfile.TemporaryDirectory() as tmp:
        repo = pathlib.Path(tmp)
        cases = {
            # clean: genuinely distinct Sanskrit, a real translation, no Latin
            "clean": [{"number": i, "text": body(i), "english": f"Agni is invoked, verse {i}.",
                       "status": "translated"} for i in range(1, 61)],
            # template: ONE body, only the counter varying -- the deva_keralam shape (G62)
            "template": [{"number": i, "text": f"{real} १२ {i}",
                          "english": f"Agni is invoked, verse {i}.", "status": "translated"}
                         for i in range(1, 61)],
            # echo: english IS the Sanskrit behind a prefix -- the mayamata shape
            "echoed": [{"number": i, "text": body(i),
                        "english": f"Classical verse translation (x {i}): {body(i)}",
                        "status": "translated"} for i in range(1, 61)],
            # nosanskrit: a translation with no source
            "nosource": [{"number": i, "text": "", "english": f"Agni is invoked, verse {i}.",
                          "status": "translated"} for i in range(1, 61)],
        }
        for name, verses in cases.items():
            d = repo / name
            d.mkdir(parents=True)
            (d / f"{name}.json").write_text(
                json.dumps(_text(name, verses), ensure_ascii=False), encoding="utf-8")

        rows = {r["id"]: r for r in measure(repo, {})}
        for r in rows.values():
            r["score"] = score(r)

        failures = []
        if len(rows) != 4:
            failures.append(f"built 4 texts, measured {len(rows)}")
        if rows.get("clean", {}).get("score", 99) >= 1:
            failures.append(f"the CLEAN text scored {rows['clean']['score']:.0f}, expected < 1")
        if rows.get("template", {}).get("skel", 1) >= 0.9:
            failures.append(f"template skel={rows['template']['skel']:.2f}, expected < 0.9")
        if rows.get("echoed", {}).get("echo", 0) < 0.99:
            failures.append(f"echoed echo={rows['echoed']['echo']:.2f}, expected ~1.00")
        if rows.get("nosource", {}).get("noSa", 0) < 0.99:
            failures.append(f"nosource noSa={rows['nosource']['noSa']:.2f}, expected ~1.00")
        for name in ("template", "echoed", "nosource"):
            if rows.get(name, {}).get("score", 0) < 1:
                failures.append(f"{name} scored {rows[name]['score']:.0f}, expected >= 1")

        for name in ("clean", "template", "echoed", "nosource"):
            if name in rows:
                r = rows[name]
                print(f"  {name:10} skel={r['skel']:.2f} echo={r['echo']:.2f} "
                      f"noSa={r['noSa']:.2f} score={r['score']:.0f}")
        if failures:
            print("\nSELFTEST FAILED:", file=sys.stderr)
            for f in failures:
                print(f"  - {f}", file=sys.stderr)
            return 1
        print("\nselftest OK: the clean text scores 0 and each defect shape fires its own signal.")
        return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=None, help="corpus root (default: this script's repo)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each signal fires on a corpus defective by construction")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    repo = pathlib.Path(args.repo) if args.repo else pathlib.Path(__file__).resolve().parent.parent
    registry = read_registry(repo)
    if len(registry) < MIN_ROWS:
        print(f"FLOOR: parsed {len(registry)} registry rows (< {MIN_ROWS}). The parser has gone "
              "blind; it has not found an empty registry.", file=sys.stderr)
        return 2

    rows = measure(repo, registry)
    if len(rows) < MIN_TEXTS:
        print(f"FLOOR: walked {len(rows)} texts (< {MIN_TEXTS}). The walker found almost nothing.",
              file=sys.stderr)
        return 2

    for r in rows:
        r["score"] = score(r)
    print(f"{len(rows)} texts checked against {len(registry)} registry rows\n")
    return render(rows)


if __name__ == "__main__":
    raise SystemExit(main())
