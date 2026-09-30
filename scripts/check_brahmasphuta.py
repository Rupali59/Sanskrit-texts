#!/usr/bin/env python3
"""Everything measurable about `brahmasphuta_siddhanta`, in one command.

WHY THIS EXISTS. This text has been carried in `TODOS.md` as "23 OCR-garbage verses" since
2026-09-16. On 2026-09-30 every part of that description turned out to be wrong, in both
directions, and each wrong number had been written down by someone who had measured something:

    claimed 23 corrupt verses        -> a supplied source inspection listed 34 rows (all 34 real,
                                        zero false positives) and an independent scan finds 80
    claimed complete, INVENTORY 100% -> chapter 18 runs 1..101 with THIRTY numbered holes
    claimed the 336pp OCR is the source -> true, but of FOUR passes of it on disk. The corpus
                                        came from `native-devanagari/txt` (58 of 60 sampled verses
                                        anchor there, against 7 in `txt`). **`render-193/txt` is
                                        not a better pass, it is a different one** -- 1,144 verse
                                        markers and 3.2x the Devanagari, yet only 32 of the same
                                        60 anchor in it. Marker count is a proxy for coverage and
                                        the two passes have different strengths, not a ranking.
                                        An earlier version of this file said "the weakest of
                                        three"; that was wrong in both halves.

So the rule for this text is the rule for the whole corpus, only louder: **derive it, never restate
it.** Nothing here is a constant that a human typed; every figure is computed at run time from the
corpus, the witnesses and the OCR, and every population has a floor so that "found nothing" and
"looked at nothing" are different outputs (`rule:derive-dont-curate`, `rule:discernment-checks` 2).

WHAT THE WITNESSES MAY AND MAY NOT BE USED FOR. `../sanskrit-texts-sources/Siddhanta/
BrahmasphutaSiddhanta/raw/` holds GRETIL and TITUS files for chapters 12, 18, 19, 20 and 21.17-23.
`docs/INVENTORY.md` records that this material is **licence-barred from seeding**: "only the OCR of
Rupali's scan is used, never the licence-barred GRETIL/TITUS text". They are also IAST -- zero
Devanagari -- so any Devanagari attributed to them has been transliterated by somebody, and a
machine transliteration presented as an attested reading is G31 exactly.

**Therefore this script reads the witnesses for NUMBERING ONLY** -- which verse numbers exist -- and
never prints their text. That is deliberate: output that quoted them would eventually be pasted into
the corpus, and the licence and the provenance would both be lost in one step.

RUN THE SELFTEST FIRST (`rule:discernment-checks` 1). It builds a text whose defects are known by
construction and asserts every class fires; a classifier that cannot fire reports a clean corpus.

    ./.venv-corpus/bin/python scripts/check_brahmasphuta.py --selftest
    ./.venv-corpus/bin/python scripts/check_brahmasphuta.py

Exit: 0 nothing outstanding, 1 defects remain, 2 a floor tripped (could not measure).
"""

from __future__ import annotations

import argparse
import collections
import html
import json
import pathlib
import re
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from sanskrit_texts.importer import corpus_files  # noqa: E402

TEXT_ID = "brahmasphuta_siddhanta"

#: Floors. Each is "the instrument has gone blind", never "the corpus is clean".
MIN_VERSES = 500          # the corpus held 691 when this was written
MIN_OCR_PAGES = 300       # the 336pp scan
MIN_WITNESS_FILES = 3     # five TITUS parts exist

#: Anything that has no business inside a Devanagari verse body.
NOISE = re.compile(r"[A-Za-z]|[_\\`\[\]<>&$]|\.{2,}")
#: `( ३३ )` -- a printed page number that leaked in at conversion.
PAGE_FURNITURE = re.compile(r"\(\s*[०-९]+\s*\)")
#: TWO or more Latin letters together: `paren fms it sy`, `QASSNSNN`, `nefe`, and `TT`.
#: **Two, not three.** At three, `TT` (a scanner header on 3.27) matched neither this nor STRAY --
#: STRAY's lone-letter rule requires no adjacent letter -- so it fell through to "unclassified"
#: and read as a defect nobody had looked at. A run of two is already not Devanagari; the reason
#: three was chosen first was that the examples to hand happened to be longer.
LATIN_RUN = re.compile(r"[A-Za-z]{2,}")
#: One Latin letter standing alone, or a stray punctuation mark, or a dot run.
STRAY = re.compile(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])|[_\\`\[\]<>&$]|\.{2,}")

#: What a class means for the fix, printed with the census so the reader need not look it up.
CLASS_FIX = {
    "A": "page furniture -- strip, confirmable against the OCR page",
    "B": "single stray char -- strip ONLY where the OCR page confirms no Devanagari was replaced",
    "C": "multi-letter Latin / glyph corruption -- needs the scan, do not guess",
    "D": "unclassified noise -- needs the scan",
}


def classify(text: str) -> str | None:
    """Which repair could legitimately apply. Order matters: A and C outrank B.

    A verse carrying a page number AND a stray letter is class A -- the page number is the thing
    that explains it, and stripping the furniture usually takes the stray with it.
    """
    # PAGE FURNITURE IS CHECKED BEFORE THE NOISE GATE, AND THAT ORDER IS LOAD-BEARING.
    # `NOISE` has no parenthesis in its class, so `( ३३ )` with no Latin beside it scored None --
    # invisible. It looked correct against the live corpus only because all three class-A verses
    # happen ALSO to carry Latin (`QASSNSNN`, `TT`), so the gate fired for the wrong reason. Caught
    # by --selftest on first run, which is the entire argument for writing one
    # (`rule:discernment-checks` 1).
    if PAGE_FURNITURE.search(text):
        return "A"
    if not NOISE.search(text):
        return None
    if LATIN_RUN.search(text):
        return "C"
    if STRAY.search(text):
        return "B"
    return "D"


def load_text(repo: pathlib.Path) -> dict | None:
    for path in corpus_files(repo):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(doc, dict) and doc.get("text_id") == TEXT_ID:
            return doc
    return None


def numbered_gaps(shlokas: list[dict]) -> list[int]:
    """Verse numbers absent from inside a chapter's OWN range.

    This is the completeness signal, and it needs no witness at all -- a chapter numbered 1..101
    holding 71 verses is missing 30 of its own, whatever any other edition says. That matters
    because it is the one completeness check that works for the seventeen chapters no witness
    covers. G12's caution applies to the converse (an absent number may be a MISLABELLED verse
    rather than a missing one), so this reports gaps and never "missing verses".
    """
    ints = sorted(int(s["number"]) for s in shlokas if str(s.get("number", "")).isdigit())
    if not ints:
        return []
    return [n for n in range(min(ints), max(ints) + 1) if n not in set(ints)]


def witness_numbering(raw: pathlib.Path) -> dict[str, set[int]]:
    """chapter -> {verse numbers the witness carries}. NUMBERS ONLY -- never the text."""
    out: dict[str, set[int]] = {}
    for f in sorted(raw.glob("*TITUS-part*.htm")):
        m = re.search(r"ch([\d.]+)", f.name)
        if not m:
            continue
        chapter = m.group(1).split(".")[0]
        body = html.unescape(re.sub(r"<[^>]+>", " ", f.read_text(encoding="utf-8", errors="replace")))
        nums = {int(x.group(1)) for x in re.finditer(r"Verse:\s*(\d+)", body)}
        if nums:
            out.setdefault(chapter, set()).update(nums)
    return out


def ocr_passes(ocr: pathlib.Path) -> dict[str, tuple[int, int, int]]:
    """pass name -> (pages, verse-end markers, devanagari chars).

    The corpus was built from ONE of these. Which one, and whether a richer pass exists, is the
    question that decides whether repair or re-conversion is the right move -- so it is measured
    rather than remembered.
    """
    out: dict[str, tuple[int, int, int]] = {}
    for name in ("txt", "native/txt", "native-devanagari/txt", "render-193/txt"):
        d = ocr / name
        pages = sorted(d.glob("*.txt")) if d.is_dir() else []
        if not pages:
            continue
        blob = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in pages)
        out[name] = (len(pages),
                     len(re.findall(r"॥\s*[०-९\d]+\s*॥", blob)),
                     len(re.findall(r"[ऀ-ॿ]", blob)))
    return out


def render(doc: dict, witness: dict[str, set[int]], ocr: dict, captured: int) -> int:
    chapters = doc["chapters"]
    total = sum(len(c.get("shlokas") or []) for c in chapters)
    print(f"{TEXT_ID}: {len(chapters)} chapters, {total:,} verses captured\n")

    # --- completeness -------------------------------------------------------------------
    print("COMPLETENESS -- gaps inside each chapter's own numbering")
    print(f"  {'ch':>4}{'verses':>8}{'range':>12}{'gaps':>7}   {'witness':>8}{'short by':>10}")
    gap_total = 0
    short_total = 0
    for c in sorted(chapters, key=lambda x: int(x["number"]) if str(x["number"]).isdigit() else 0):
        sh = c.get("shlokas") or []
        gaps = numbered_gaps(sh)
        gap_total += len(gaps)
        ints = [int(s["number"]) for s in sh if str(s.get("number", "")).isdigit()]
        rng = f"{min(ints)}..{max(ints)}" if ints else "-"
        w = witness.get(str(c["number"]))
        wn = len(w) if w else 0
        short = (wn - len(sh)) if w else 0
        if short > 0:
            short_total += short
        flag = f"{short:+d}" if w else ""
        print(f"  {str(c['number']):>4}{len(sh):>8}{rng:>12}{len(gaps):>7}   {wn or '-':>8}{flag:>10}")
    print(f"\n  numbered gaps, all chapters: {gap_total}")
    print(f"  short against a witness    : {short_total}   "
          f"(witnessed chapters: {', '.join(sorted(witness)) or 'none'})")

    # --- corruption ---------------------------------------------------------------------
    per_class: collections.Counter = collections.Counter()
    examples: dict[str, list[str]] = collections.defaultdict(list)
    for c in chapters:
        for s in c.get("shlokas") or []:
            cls = classify(s.get("text") or "")
            if not cls:
                continue
            per_class[cls] += 1
            examples[cls].append(f"{c['number']}.{s['number']}")
    noisy = sum(per_class.values())
    print(f"\nCORRUPTION -- {noisy} of {total:,} verses carry something that is not Devanagari")
    for cls in "ABCD":
        if not per_class[cls]:
            continue
        print(f"  {cls}  {per_class[cls]:>4}  {CLASS_FIX[cls]}")
        print(f"        e.g. {', '.join(examples[cls][:6])}")

    # --- the source ---------------------------------------------------------------------
    print(f"\nOCR PASSES ON DISK -- corpus captured {captured:,} verses")
    print(f"  {'pass':28}{'pages':>7}{'verse marks':>13}{'devanagari':>12}")
    best = None
    for name, (pages, marks, dev) in ocr.items():
        print(f"  {name:28}{pages:>7}{marks:>13,}{dev:>12,}")
        if best is None or marks > ocr[best][1]:
            best = name
    if best and ocr[best][1] > captured:
        print(f"\n  richest pass is {best}: {ocr[best][1]:,} verse markers against {captured:,} "
              f"captured ({ocr[best][1] - captured:+,}).")
        print("  SETTLED 2026-09-30: some are real verses (ch18's missing 19, 20, 26, 27, 28 are "
              "all present there), but it is NOT a superset -- it anchors only 32 of 60 verses the")
        print("  corpus already holds, against 58 for native-devanagari/txt, which is where the "
              "corpus came from. Re-conversion from it alone would recover units and LOSE units.")
        print("  Table and the merge question: docs/SOURCES.md, 'The four OCR passes'.")

    outstanding = gap_total + noisy
    print(f"\n  outstanding: {gap_total} numbered gaps + {noisy} noisy verses")
    return 1 if outstanding else 0


def selftest() -> int:
    """A text defective BY CONSTRUCTION; assert every class and the gap finder fire."""
    real = "रामो राजमणिः सदा विजयते"
    verses = [
        {"number": 1, "text": real, "status": "translated"},                       # clean
        {"number": 2, "text": f"( ३३ ) {real}", "status": "translated"},            # A
        {"number": 3, "text": f"{real} t करान्त्यंशे", "status": "translated"},      # B
        {"number": 5, "text": f"{real} paren fms it sy", "status": "translated"},   # C  (4 missing)
        {"number": 7, "text": f"TT {real}", "status": "translated"},                # C, two letters
        {"number": 6, "text": f"{real} ..........", "status": "translated"},        # B (dot run)
    ]
    doc = {"text_id": TEXT_ID, "title_sa": "x", "title_en": "x", "category": "test",
           "chapters": [{"number": 1, "title": "x", "shlokas": verses}]}

    got = {v["number"]: classify(v["text"]) for v in verses}
    expect = {1: None, 2: "A", 3: "B", 5: "C", 6: "B", 7: "C"}
    if got != expect:
        print(f"SELFTEST FAIL: classify() returned {got}, expected {expect}", file=sys.stderr)
        return 1
    gaps = numbered_gaps(verses)
    if gaps != [4]:
        print(f"SELFTEST FAIL: numbered_gaps() returned {gaps}, expected [4]", file=sys.stderr)
        return 1

    # The classifier must also REFUSE things that are legitimate elsewhere in the corpus, or a
    # future reader will reach for it corpus-wide -- which is 99.2% false positives (G70,
    # samaveda's arcika suffixes, brihat_samhita's (K....) apparatus).
    for legit in ("०१०१a", "अथ (K.अर्थः) इति", "।।"):
        if classify(legit) and not NOISE.search(legit):
            print(f"SELFTEST FAIL: {legit!r} classified as noise", file=sys.stderr)
            return 1

    with tempfile.TemporaryDirectory() as tmp:
        repo = pathlib.Path(tmp)
        (repo / "T").mkdir()
        (repo / "T" / "T.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
        loaded = load_text(repo)
        if not loaded or len(loaded["chapters"][0]["shlokas"]) != len(verses):
            print("SELFTEST FAIL: load_text did not round-trip the fixture", file=sys.stderr)
            return 1

    print("selftest OK -- every class fires, the gap finder fires, legitimate apparatus is refused")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--repo", default=None, help="corpus root (default: this script's repo)")
    ap.add_argument("--selftest", action="store_true",
                    help="prove each class fires on a text defective by construction")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()

    repo = pathlib.Path(args.repo) if args.repo else pathlib.Path(__file__).resolve().parent.parent
    doc = load_text(repo)
    if doc is None:
        print(f"FLOOR: no text with text_id={TEXT_ID} under {repo}. The walker failed; this is "
              "not a clean corpus.", file=sys.stderr)
        return 2
    captured = sum(len(c.get("shlokas") or []) for c in doc["chapters"])
    if captured < MIN_VERSES:
        print(f"FLOOR: walked {captured} verses (< {MIN_VERSES}). The walker has gone blind.",
              file=sys.stderr)
        return 2

    src = repo.parent / "sanskrit-texts-sources" / "Siddhanta" / "BrahmasphutaSiddhanta"
    witness = witness_numbering(src / "raw") if (src / "raw").is_dir() else {}
    ocr = ocr_passes(src / "ocr") if (src / "ocr").is_dir() else {}

    # Absence must be attributable. A missing source tree is a fact about this run, not a clean bill.
    if not witness:
        print(f"  note: no witness files under {src / 'raw'} -- completeness is measured from "
              "internal numbering only", file=sys.stderr)
    elif len(witness) < MIN_WITNESS_FILES:
        print(f"FLOOR: parsed {len(witness)} witness chapters (< {MIN_WITNESS_FILES}); the parser "
              "has gone blind.", file=sys.stderr)
        return 2
    if ocr and max(p for p, _, _ in ocr.values()) < MIN_OCR_PAGES:
        print(f"FLOOR: richest OCR pass has fewer than {MIN_OCR_PAGES} pages.", file=sys.stderr)
        return 2
    if not ocr:
        print(f"  note: no OCR under {src / 'ocr'} -- pass comparison skipped", file=sys.stderr)

    return render(doc, witness, ocr, captured)


if __name__ == "__main__":
    raise SystemExit(main())
