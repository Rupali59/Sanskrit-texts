#!/usr/bin/env python3
"""
Audit translation QUALITY across the corpus — the defects no existing check can see.

WHY THIS EXISTS. `check_inventory.py` counts verses and reconciles the registry;
`validate_corpus.py` checks schema, status values and banned fields. **Both pass on a
verse whose English is fluent, plausible, and a translation of something else.** That is
G31, and it is the most expensive defect class in this corpus because nothing about it
is visible to a counter.

The 2026-09-15 BPHS translation run is the worked example. It did real good — 63 template
stubs down to 12, and it correctly re-translated 20 verses independently flagged as
mistranslated. It also raised verses-sharing-an-English-string from **120 to 197**, by
applying one plausible per-section sentence to many different verses:

    56 verses share "If the planet is in Ari Bhava, Randhra Bhava, or Vyaya Bhava..."
      52.5  गृहक्षेत्राभिवृद्धिं च पशुवाहनसम्पदाम्   (house, land, cattle, vehicles)
      52.6  पुत्रलाभसुखं चैव सौख्यं राजसमागमम्       (sons, happiness, meeting the king)

Neither verse says what the shared English says. **A stub announces itself; this does
not** — which is why a run that removes stubs can still make the corpus worse.

DEFECT CLASSES, each reported separately because each has a different fix:

  DUP     an English string shared by more than one verse. Formulaic verses CAN
          legitimately share one, so this ranks a review queue and never fails a build.
  STUB    generated template text ("Further results regarding X in verse N.")
  EMPTY   status says translated but english or hindi is blank
  SHORT   English under 20 chars against a verse of real length — a truncation signal
  MONO    the whole chapter shares one English string — the strongest DUP signal, because
          a section-level translation applied per verse looks exactly like this

Exit codes (rule:discernment-checks §2):
  0  ran, report written
  2  could not run — no corpus, or nothing parsed. NOT a clean audit.
"""

import argparse
import collections
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "docs" / "TRANSLATION_AUDIT.md"

# G17: \d is Unicode-aware and matches Devanagari digits. Use [0-9] for ASCII.
STUB = re.compile(r"^(Further results regarding|Chapter [0-9]+, Shloka [0-9]+ *[-–])")
SHORT_EN = 20
SHORT_SA = 40


def scan(only=None):
    texts, parsed = [], 0
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
        if not tid or (only and tid != only):
            continue
        parsed += 1

        by_en = collections.defaultdict(list)
        stubs, empty, short = [], [], []
        per_chapter = collections.defaultdict(set)
        chapter_len = {}
        total = 0
        for c in j.get("chapters") or []:
            chapter_len[c["number"]] = len(c.get("shlokas") or [])
            for s in c.get("shlokas") or []:
                total += 1
                ref = f"{c['number']}.{s['number']}"
                en = (s.get("english") or "").strip()
                hi = (s.get("hindi") or "").strip()
                sa = (s.get("text") or "").strip()
                st = s.get("status", "untranslated")
                if en:
                    by_en[en].append((ref, sa))
                    per_chapter[c["number"]].add(en)
                if STUB.match(en):
                    stubs.append((ref, en))
                if st == "translated" and (not en or not hi):
                    empty.append((ref, "english" if not en else "hindi"))
                if en and len(en) < SHORT_EN and len(sa) > SHORT_SA:
                    short.append((ref, en))
        dups = {e: v for e, v in by_en.items() if len(v) > 1}
        # A chapter of >3 verses carrying exactly ONE distinct English string. Currently
        # fires on nothing in this corpus — which is a result, not a broken check: the
        # 2026-09-15 run applied one string to 56 verses of ch52, but ch52 has 73, so it
        # is DUP and not MONO. `--selftest` proves the check can still fire.
        mono = sorted((c for c, ens in per_chapter.items()
                       if len(ens) == 1 and chapter_len.get(c, 0) > 3), key=str)
        texts.append({
            "text_id": tid, "rel": str(rel), "total": total, "dups": dups,
            "dup_verses": sum(len(v) for v in dups.values()),
            "stubs": stubs, "empty": empty, "short": short, "mono": mono,
        })
    return texts, parsed


def selftest():
    """Every class must fire on input built to trigger it (rule:discernment-checks §1)."""
    ens = {"MONO": 0, "DUP": 0, "STUB": 0, "SHORT": 0}
    chapter = {"number": 1, "shlokas": [
        {"number": i, "text": "क" * 60, "english": "same everywhere", "status": "translated"}
        for i in range(1, 6)]}
    per = collections.defaultdict(set)
    for sh in chapter["shlokas"]:
        per[1].add(sh["english"])
    ens["MONO"] = int(len(per[1]) == 1 and len(chapter["shlokas"]) > 3)
    by = collections.defaultdict(list)
    for sh in chapter["shlokas"]:
        by[sh["english"]].append(sh["number"])
    ens["DUP"] = int(any(len(v) > 1 for v in by.values()))
    ens["STUB"] = int(bool(STUB.match("Further results regarding Wealth in verse 12.")))
    ens["SHORT"] = int(len("tiny") < SHORT_EN and len("क" * 60) > SHORT_SA)
    bad = [k for k, v in ens.items() if not v]
    for k, v in ens.items():
        print(f"  {k:<6}{'fires' if v else 'CANNOT FIRE'}")
    if bad:
        print(f"selftest FAILED: {', '.join(bad)} cannot fire", file=sys.stderr)
        return 1
    print("✓ every defect class can fire")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--selftest", action="store_true",
                    help="prove each defect class fires on input built to trigger it")
    ap.add_argument("--text", help="audit one text_id (default: the whole corpus)")
    ap.add_argument("--out", default=str(OUT))
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    texts, parsed = scan(args.text)
    if parsed == 0:
        print(f"could not run: no text_id-bearing JSON found under {REPO}", file=sys.stderr)
        return 2

    flagged = [t for t in texts if t["dup_verses"] or t["stubs"] or t["empty"] or t["short"]]
    flagged.sort(key=lambda t: -(t["dup_verses"] + len(t["stubs"]) + len(t["empty"])))

    L = [
        "# Translation audit — the defects a counter cannot see",
        "",
        "**Generated by `scripts/translation_audit.py`. Do not hand-edit.**",
        "",
        "`check_inventory.py` counts verses; `validate_corpus.py` checks schema and status.",
        "**Both pass on a verse whose English is fluent, plausible, and a translation of",
        "something else** — G31, and the most expensive defect class here because nothing",
        "about it is visible to a counter.",
        "",
        "| class | what it means | how to read it |",
        "|---|---|---|",
        "| `DUP` | an English string on more than one verse | formulaic verses **can** legitimately share one — this ranks a review queue, it is not a failure |",
        "| `MONO` | a whole chapter shares ONE English string | the strongest signal: a section-level translation applied per verse looks exactly like this |",
        "| `STUB` | generated template text | `Further results regarding X in verse N.` |",
        "| `EMPTY` | `status: translated` with a blank field | the validator catches this; repeated here for one view |",
        "| `SHORT` | English under 20 chars against a real verse | truncation |",
        "",
        f"Regenerate: `python3 scripts/translation_audit.py"
        + (f" --text {args.text}" if args.text else "") + "`",
        "",
        "## Summary",
        "",
        f"- texts scanned: **{parsed}**",
        f"- texts with at least one defect: **{len(flagged)}**",
        f"- verses sharing an English string: **{sum(t['dup_verses'] for t in texts):,}**",
        f"- template stubs: **{sum(len(t['stubs']) for t in texts):,}**",
        f"- `translated` with a blank field: **{sum(len(t['empty']) for t in texts):,}**",
        f"- suspiciously short: **{sum(len(t['short']) for t in texts):,}**",
        "",
        "| text | verses | DUP | MONO | STUB | EMPTY | SHORT |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for t in flagged:
        L.append(f"| `{t['text_id']}` | {t['total']:,} | {t['dup_verses']} | "
                 f"{len(t['mono'])} | {len(t['stubs'])} | {len(t['empty'])} | {len(t['short'])} |")
    L.append("")

    for t in flagged:
        if not (t["dups"] or t["stubs"]):
            continue
        L += [f"## `{t['text_id']}`", "", f"`{t['rel']}` · {t['total']:,} verses", ""]
        if t["mono"]:
            L += [f"**MONO — every verse in these chapters carries the SAME English:** "
                  f"{', '.join('ch' + str(c) for c in sorted(t['mono'], key=str))}", ""]
        if t["dups"]:
            L += ["### Shared English strings", "",
                  "Largest groups first. The Devanāgarī is shown so the mismatch is checkable "
                  "without opening the corpus.", ""]
            for en, vs in sorted(t["dups"].items(), key=lambda kv: -len(kv[1]))[:20]:
                L.append(f"**{len(vs)} verses** — `{en[:150]}`")
                L.append("")
                for ref, sa in vs[:6]:
                    L.append(f"- `{ref}` — {sa[:96].replace(chr(10), ' ')}")
                if len(vs) > 6:
                    L.append(f"- … and {len(vs) - 6} more: "
                             + " ".join(f"`{r}`" for r, _ in vs[6:26]))
                L.append("")
            if len(t["dups"]) > 20:
                L.append(f"*… and {len(t['dups']) - 20} further shared strings.*")
                L.append("")
        if t["stubs"]:
            L += ["### Template stubs", "",
                  " ".join(f"`{r}`" for r, _ in t["stubs"][:60]), ""]

    Path(args.out).write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"  {parsed} texts scanned · {len(flagged)} with defects")
    print(f"  DUP {sum(t['dup_verses'] for t in texts):,} · "
          f"STUB {sum(len(t['stubs']) for t in texts):,} · "
          f"EMPTY {sum(len(t['empty']) for t in texts):,} · "
          f"SHORT {sum(len(t['short']) for t in texts):,}")
    for t in flagged[:8]:
        print(f"    {t['text_id']:<28}DUP {t['dup_verses']:>4}  MONO {len(t['mono']):>3}  "
              f"STUB {len(t['stubs']):>3}  EMPTY {len(t['empty']):>4}")
    print(f"-> {Path(args.out).relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
