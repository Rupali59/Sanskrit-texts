#!/usr/bin/env python3
"""
Write the mahadasa label onto BPHS chapters 52-60 — 690 verses, positionally exact.

WHAT THIS SHIPS, AND WHAT IT DELIBERATELY DOES NOT.

  SHIPS   `mahadasha:<slug>` — which graha's mahadasa a verse sits under.
  DOES NOT SHIP  the antardasa label. Measured 2026-09-14 and rejected; see below.

WHY THE MAHADASA LABEL IS SAFE. Three independent sources agree on it for all nine
chapters, so it is verified rather than inferred:

  1. the chapter title            ch52 = अथ विंशोत्तरीमतेन सूर्यदशान्तर्दशाफलाध्यायः
  2. the anchor formula in-verse  सूर्यस्यान्तर्गते, 8x inside that same chapter
  3. the ORDER of the nine chapters is exactly Vimsottari (Sun, Moon, Mars, Rahu,
     Jupiter, Saturn, Mercury, Ketu, Venus)

This script re-derives 1 and 2 on every run and REFUSES to write if they disagree
anywhere. A title alone would be a single point of failure; the cross-check is the
reason this is not just "trust the heading".

WHY THE ANTARDASA LABEL IS NOT HERE. The plan priced it as the cheap win: 78
`X-स्यान्तर्गते` anchors segmenting 9 chapters into 81 (mahadasa, antardasa) cells
"at 100% Vimsottari agreement". That 100% was CIRCULAR — the labels were assigned by
walking Vimsottari order, then checked against Vimsottari order.

Two things then came out of reading the actual strings:

  * The anchor names the MAHADASA lord, not the antardasa lord. Every one of ch52's
    eight anchors reads सूर्यस्यान्तर्गते, in the Sun's own chapter. So the anchors
    give BOUNDARIES and no label at all.
  * Checked non-circularly — does each run NAME the graha positionally assigned to it
    — agreement is 40.6%. Fitting one free offset per chapter, to the same signal
    being used to score it, reaches only 66.2%. That is an upper bound, not a result.

The structural reason is worth keeping: phala verses describe RESULTS, not grahas.
Evidence runs at 1-5 graha mentions per 6-13 verse run, because the graha is named at
the boundary and everything after it is effects. There is very little content to
validate against, by construction — so the antardasa axis needs a Sanskrit reader,
not a better heuristic.

Exit codes (rule:discernment-checks §2):
  0  ran
  1  refused — title and anchors disagree, or the key set moved
  2  could not run — corpus absent, unparseable, or chapters missing
"""

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BPHS = REPO / "Hora/Parashari/BrihatParasharaHoraShastra/BrihatParasharaHoraShastra.json"

# astroacharya seeds/grahas.json slugs — matched deliberately so a tag written here
# joins to the entity table there without a translation step.
VIMSOTTARI = ["sun", "moon", "mars", "rahu", "jupiter", "saturn", "mercury", "ketu", "venus"]

# Chapter-title stems. रह्व / शन्य / केत्व are SANDHI-FUSED (राहु+अन्तर्, शनि+अन्तर्,
# केतु+अन्तर्), which is why a naive root scan misses three of the nine chapters.
TITLE_STEM = {"सूर्य": "sun", "चन्द्र": "moon", "कुज": "mars", "रह्व": "rahu",
              "जीव": "jupiter", "शन्य": "saturn", "बुध": "mercury",
              "केत्व": "ketu", "शुक्र": "venus"}

# In-verse anchor stems — a SEPARATE vocabulary from the titles on purpose. मन्द for
# Saturn and सौम्य for Mercury appear only here, and that non-overlap is what makes
# the cross-check independent rather than a restatement of the title.
ANCHOR_STEM = {"सूर्य": "sun", "चन्द्र": "moon", "कुज": "mars", "राहु": "rahu",
               "राहो": "rahu", "जीव": "jupiter", "मन्द": "saturn", "बुध": "mercury",
               "सौम्य": "mercury", "केतो": "ketu", "केतु": "ketu", "शुक्र": "venus"}

ANCHOR = re.compile(r"[ऀ-ॣ॰-ॿ]*न्तर्गते")
CHAPTERS = range(52, 61)


def key_set(doc):
    """Every (chapter, shloka) in the file. Compared as a SET, never a count — a pass
    that drops one verse and adds another survives a length check. Two such bugs
    happened in one translation run on 2026-09-14 (dhanurveda 227->2, panchasiddhantika
    lost 5 from the middle)."""
    return {(c["number"], s["number"]) for c in doc["chapters"] for s in c["shlokas"]}


def derive(doc):
    """Return {chapter_number: slug}, or (None, reason) if the two sources disagree."""
    out, problems = {}, []
    for ch in doc["chapters"]:
        n = ch["number"]
        if n not in CHAPTERS:
            continue
        from_title = next((v for k, v in TITLE_STEM.items() if k in ch.get("title", "")), None)
        from_anchor = set()
        for sh in ch["shlokas"]:
            for m in ANCHOR.finditer(sh.get("text", "")):
                w = m.group(0)
                for k, v in ANCHOR_STEM.items():
                    if w.startswith(k):
                        from_anchor.add(v)
                        break
        if from_title is None:
            problems.append(f"ch{n}: no graha stem in title {ch.get('title','')!r}")
        elif from_anchor and from_anchor != {from_title}:
            problems.append(f"ch{n}: title says {from_title}, anchors say {sorted(from_anchor)}")
        else:
            out[n] = from_title
    missing = [n for n in CHAPTERS if n not in out]
    if missing and not problems:
        problems.append(f"chapters absent from the corpus: {missing}")
    return out, problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--apply", action="store_true",
                    help="write the file; without it NOTHING is written")
    args = ap.parse_args()

    if not BPHS.exists():
        print(f"could not run: {BPHS} does not exist", file=sys.stderr)
        return 2
    try:
        doc = json.loads(BPHS.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        print(f"could not run: {BPHS} does not parse: {e}", file=sys.stderr)
        return 2

    before = key_set(doc)
    mapping, problems = derive(doc)
    if problems:
        print("REFUSING — the two sources disagree, so the label is not verified:",
              file=sys.stderr)
        for p in problems:
            print(f"  {p}", file=sys.stderr)
        return 1

    changed = 0
    for ch in doc["chapters"]:
        if ch["number"] not in mapping:
            continue
        tag = f"mahadasha:{mapping[ch['number']]}"
        for sh in ch["shlokas"]:
            tags = sh.get("tags") or []
            if tag not in tags:
                sh["tags"] = tags + [tag]      # merge, never overwrite
                changed += 1

    after = key_set(doc)
    if after != before:
        added, dropped = after - before, before - after
        print(f"REFUSING — the key set moved: +{len(added)} -{len(dropped)}", file=sys.stderr)
        return 1

    for n in CHAPTERS:
        ch = next(c for c in doc["chapters"] if c["number"] == n)
        print(f"  ch{n:>3}  {mapping[n]:<8} {len(ch['shlokas']):>3} verses  "
              f"mahadasha:{mapping[n]}")
    print(f"\n  {changed} verses tagged · key set unchanged ({len(before):,} keys)")

    if not args.apply:
        print("  DRY RUN — nothing written. Re-run with --apply.")
        return 0

    BPHS.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    reread = json.loads(BPHS.read_text(encoding="utf-8"))   # must parse after write
    if key_set(reread) != before:
        print("WROTE A FILE WHOSE KEY SET MOVED — restore from git", file=sys.stderr)
        return 1
    print("  WRITTEN and re-parsed OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
