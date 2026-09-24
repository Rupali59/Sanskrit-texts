#!/usr/bin/env python3
"""
Derive the translation backlog per text.

`docs/TRANSLATION_BACKLOG.md` names this script instead of restating its numbers, per
rule:state-and-decisions — a count in a doc rots faster than anything else in it.

FOUR different jobs are reported separately, because handing them out as one produces
wrong work:

  UNTR   untranslated -- `english` is empty. Translate it.
  DRAFT  a real per-verse English draft sits in `english_draft`. VERIFY and promote;
         never copy across unread.
  ECHO   `english_draft` is NOT a translation -- it holds the verse's own Sanskrit and/or
         a label repeated across the text. **Translate it.** There is nothing to verify.
  STUB   `status: translated` but `english` is a generated template, not a translation.
         RE-translate. The worker is replacing text, not filling a blank.

**ECHO was split out of DRAFT on 2026-09-23, and the split changed the backlog by sixty-fold.**
Every draft counted as work-in-progress; reading them showed 67,965 of 69,037 contained no
English at all. The typical case is `astanga_hridaya`:

    Classical text translation of Astanga Hridaya: <the Sanskrit verse, verbatim>

These are the 67,820 non-translations taken off the served fields on 2026-09-16 (`9ce801e`) --
correctly parked behind the publication gate, and never translated since. Reporting them as
`VERIFY-DRAFT` read as "written, awaiting review" and understated the real work from ~68,000
to ~2,800.

**Why the classifier is shaped the way it is.** Two instruments were tried and both were wrong,
so do not "simplify" it back:

  * A distinct-skeleton ratio rated these drafts 0.95-1.00, "looks real". They score as distinct
    because the EMBEDDED SANSKRIT varies -- the distinctness never came from a translation.
    G55's lesson in a new place: a variation statistic measures variation, not content.
  * A minimum-English-word floor then classified 85 genuine `jaimini_sutra` drafts as echoes --
    *"Jupiter in the 4th gives a wooden house."* is a complete translation of a terse sutra.
    **Length does not separate them; repetition does.**

So: strip the verse's own Sanskrit, strip any Devanagari left over, and ask whether the English
that remains is verse-SPECIFIC. Boilerplate repeats across the text whatever its length; a real
translation does not.

Exit codes are distinguishable on purpose (rule:discernment-checks §2):
  0  ran, reported
  2  could not run -- no corpus found, or nothing parsed. NOT a clean backlog.

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
# `[0-9]`, never `\d` -- G17: Python's `\d` matches Devanagari digits too.
STUB_RE = re.compile(r"^Chapter [0-9]+, Shloka [0-9]+ *[-–]")

DEVANAGARI = re.compile(r"[ऀ-ॿ।॥]+")
EN_WORD = re.compile(r"[A-Za-z']{2,}")
LATIN_LETTER = re.compile(r"[A-Za-z]")

# ---------------------------------------------------------------------------
# `sanskrit_texts.checks.check_translation` is CANONICAL for the three rules in
# `fails_canonical_checks` below. They are mirrored here rather than imported because that
# module imports SQLAlchemy, while `docs/TRANSLATION_BACKLOG.md` documents this script as
# runnable under bare `python3` -- the same constraint that forced `check_inventory.py` to
# carry its own corpus walk.
#
# **A mirror is a fork unless something compares them**, so
# `tests/test_translation_backlog.py::test_the_mirrored_rules_agree_with_the_canonical_checker`
# asserts both give the same verdict on every draft in the live corpus. Change either and that
# test fails. Do not "tidy" it away.
# ---------------------------------------------------------------------------
TEMPLATE_PREFIX = re.compile(r"^Classical text translation of [^:]+: ")
SANSKRIT_ECHO_SHARE = 0.30


def devanagari_share(value: str) -> float:
    """Devanagari as a fraction of non-space characters -- `check_translation`'s measure."""
    chars = [c for c in value if not c.isspace()]
    if not chars:
        return 0.0
    return sum(1 for c in chars if "\u0900" <= c <= "\u097f") / len(chars)


def fails_canonical_checks(draft: str) -> bool:
    """The three `check_translation` `fails` reasons that can apply to an English draft."""
    return bool(
        TEMPLATE_PREFIX.match(draft)                       # template-prefix
        or devanagari_share(draft) > SANSKRIT_ECHO_SHARE   # sanskrit-echo
        or not LATIN_LETTER.search(draft)                  # wrong-script
    )


#: A skeleton shared by this many verses in one text is boilerplate, not translation.
#: 3 rather than 2 so that a pair of genuinely similar short renderings is not condemned.
#: **This rule is NOT in the canonical checker, and is why this file needs a classifier at
#: all.** `check_translation` cannot see a label written in fluent English with no
#: Devanagari and no template prefix -- `manu_smriti`'s 357 read "Scholarly English
#: translation of Chapter 4, Shloka 1, following Kulluka Bhatta and Medhatithi." and score
#: `no-defect-found`. Repetition is what exposes them.
TEMPLATE_MIN = 3


def draft_body(draft: str, sanskrit: str) -> str:
    """The English left in `draft` once the verse's own Sanskrit is removed.

    The echo drafts quote the verse verbatim after a label, so removing the verse is what
    exposes that nothing else is there. Any Devanagari surviving that (a different edition's
    reading, a stray pada) is likewise not a translation.
    """
    body = draft.replace(sanskrit, " ") if sanskrit and sanskrit in draft else draft
    return DEVANAGARI.sub(" ", body)


def skeleton(body: str) -> str:
    """Digit-insensitive fingerprint of a draft's English, for spotting a repeated label."""
    return re.sub(r"[0-9]+", "N", " ".join(EN_WORD.findall(body)).lower())


def classify_drafts(items):
    """Split (draft, sanskrit) pairs into real English drafts and echoes.

    Returns (english, echo) counts. `items` must be every draft in ONE text -- the
    repetition test is only meaningful within a single text's own vocabulary.
    """
    bodies = [draft_body(d, sa) for d, sa in items]
    counts = collections.Counter(skeleton(b) for b in bodies)
    english = echo = 0
    for (draft, _sa), b in zip(items, bodies):
        if (fails_canonical_checks(draft)
                or not EN_WORD.search(b)
                or counts[skeleton(b)] >= TEMPLATE_MIN):
            echo += 1
        else:
            english += 1
    return english, echo


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
        c, stub, drafts, mismatch = collections.Counter(), 0, [], 0
        for ch in j.get("chapters") or []:
            for s in ch.get("shlokas") or []:
                st = s.get("status", "untranslated")
                c[st] += 1
                english = (s.get("english") or "").strip()
                if st == "translated" and STUB_RE.match(english):
                    stub += 1
                d = (s.get("english_draft") or "").strip()
                if d:
                    drafts.append((d, (s.get("text") or "").strip()))
                # `status` is not evidence about the served fields, and the Mongo seeder
                # reads the FIELDS (G50). Where they disagree, say so rather than pick one.
                held = "both" if english and (s.get("hindi") or "").strip() else (
                    "one" if english or (s.get("hindi") or "").strip() else "none")
                expect = {"translated": "both", "partial": "one",
                          "untranslated": "none", "drafted": "none"}.get(st)
                if expect and held != expect:
                    mismatch += 1
        draft_en, draft_echo = classify_drafts(drafts)
        rows.append({
            "text_id": tid,
            "category": j.get("category", "?"),
            "authority": (j.get("structure") or {}).get("count_authority", ""),
            "total": sum(c.values()),
            "translated": c["translated"],
            "untranslated": c["untranslated"],
            "partial": c["partial"],
            "draft_en": draft_en,
            "draft_echo": draft_echo,
            "stub": stub,
            "mismatch": mismatch,
        })
    return rows, parsed


def main():
    rows, parsed = scan()
    if parsed == 0:
        print(f"could not run: no text_id-bearing JSON found under {REPO}", file=sys.stderr)
        return 2

    work = lambda r: r["untranslated"] + r["partial"] + r["stub"] + r["draft_echo"]
    rows.sort(key=lambda r: (work(r), r["draft_en"]), reverse=True)
    outstanding = [r for r in rows if work(r) or r["draft_en"]]

    hdr = (f'{"text_id":<30}{"category":<22}{"total":>8}{"UNTR":>8}{"part":>6}'
           f'{"ECHO":>8}{"DRAFT":>7}{"STUB":>6}  authority')
    print(hdr)
    print("-" * len(hdr))
    for r in outstanding:
        print(f'{r["text_id"]:<30}{r["category"]:<22}{r["total"]:>8,}{r["untranslated"]:>8,}'
              f'{r["partial"]:>6}{r["draft_echo"]:>8,}{r["draft_en"]:>7,}{r["stub"]:>6}'
              f'  {r["authority"]}')
    print("-" * len(hdr))

    tot = lambda k: sum(r[k] for r in rows)
    print(f'{parsed} texts scanned · {len(outstanding)} need work · '
          f'{len(rows) - len(outstanding)} complete')
    print(f'TRANSLATE {tot("untranslated") + tot("partial") + tot("draft_echo"):,} '
          f'(of which {tot("draft_echo"):,} sit in `english_draft` and are NOT translations) · '
          f'VERIFY-DRAFT {tot("draft_en"):,} · RE-TRANSLATE-STUB {tot("stub"):,} '
          f'(of {tot("total"):,} total)')

    if tot("mismatch"):
        print(f'\n⚠ {tot("mismatch"):,} verses where `status` disagrees with the served fields '
              f'— the seeder reads the FIELDS, not `status` (G50):')
        for r in sorted(rows, key=lambda r: -r["mismatch"]):
            if r["mismatch"]:
                print(f'  {r["text_id"]:<24}{r["mismatch"]:>8,}')

    by_cat = collections.Counter()
    for r in rows:
        by_cat[r["category"]] += r["untranslated"] + r["partial"] + r["draft_echo"]
    print("\nawaiting translation by category:")
    for cat, n in by_cat.most_common():
        if n:
            print(f"  {cat:<24}{n:>8,}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
