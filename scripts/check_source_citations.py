#!/usr/bin/env python3
"""Every `@source` citation in astroacharya, checked against this corpus.

WHY THIS EXISTS. `astroacharya/app/masters/_source.py`'s decorator is documentation-only: it
sets `fn.__source_refs__` and **validates nothing**, ever, in any code path. So a citation can
name a text this corpus does not hold, or a verse that does not exist in the text it does hold,
and every test in both repos still passes. Measured 2026-09-25: 115 call sites, of which 7 cite
texts absent from the corpus.

WHY `ast` AND NOT A REGEX. These are real Python decorators. A regex over the source has to
re-implement string and list literal parsing and gets `[1-25]` wrong in a way that matters --
see MALFORMED below. `ast` reads what Python reads.

THE NAME MAPPING IS THE SUBTLE PART. astroacharya writes `"Surya Siddhanta"` (a space) and
`"BPHS"` (uppercase); the corpus `text_id` is `surya_siddhanta`. `SourceRef.resolve_url` in
astroacharya did `self.text_id.lower()` and left the SPACE in, which is why that function has a
test and no callers. Normalise both halves, never one.

MALFORMED CITATIONS ARE A SEPARATE CLASS FROM MISSING ONES. `@source(("BPHS", 1, [1-25]))` is
valid Python: `[1-25]` is the one-element list `[-24]`. It reads as a range to a human and is a
negative verse number to the machine. Those are reported as MALFORMED, not as missing verses,
because the fix is different -- the citation was mistyped, not aimed at absent data.

Exit codes (rule:discernment-checks §2 -- absence must be attributable):
  0  every citation resolves
  1  at least one citation is unresolvable or malformed
  2  could not run (astroacharya not found, or no call sites parsed)
"""

from __future__ import annotations

import argparse
import ast
import collections
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from sanskrit_texts.importer import corpus_files  # noqa: E402

DEFAULT_ASTROACHARYA = pathlib.Path(__file__).resolve().parents[2] / "astroacharya"


def normalise(text_id: str) -> str:
    """`"Surya Siddhanta"` -> `surya_siddhanta`. Both halves, never one."""
    return "_".join(text_id.strip().lower().split())


def corpus_index(root: pathlib.Path) -> dict[str, set[tuple[str, str]]]:
    """text_id -> {(chapter, verse)} as STRINGS: numbers are int or str per the schema."""
    index: dict[str, set[tuple[str, str]]] = {}
    for path in corpus_files(root):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(doc, dict) or "chapters" not in doc or "text_id" not in doc:
            continue
        keys = {
            (str(ch.get("number")), str(sh.get("number")))
            for ch in doc["chapters"]
            for sh in (ch.get("shlokas") or [])
        }
        index.setdefault(normalise(doc["text_id"]), set()).update(keys)
    return index


def citations(app_root: pathlib.Path, unreadable: list[str], in_docstring: list[str]):
    """Yield (file, line, text_id, chapter, [shlokas]) for every @source ref."""
    for path in sorted(app_root.rglob("*.py")):
        try:
            src = path.read_text(encoding="utf-8")
            tree = ast.parse(src, filename=str(path))
        except (OSError, SyntaxError) as exc:
            # A file this reader cannot read is NOT a file with no citations
            # (rule:discernment-checks §2/§6). Say so; never count it as clean.
            unreadable.append(f"{path}: {exc}")
            continue

        # A `@source(...)` written INSIDE A DOCSTRING reads to a human as a citation and is
        # invisible to every tool, including astroacharya's own `__source_refs__` index.
        # Found 2026-09-25: puja_windows.py:183 cites Bhavishya_Purana this way, and a grep
        # counted it as a real call site. Report it separately -- it is a documentation
        # hazard, not a missing text.
        # NARROWED, and the narrowing is the point. A MODULE docstring containing
        # `@source((` is documentation showing the syntax, and `_source.py`'s own `source()`
        # docstring necessarily contains it. Reporting those makes every clean run carry four
        # permanent false lines, which trains the reader to skim past the real one -- the same
        # reasoning as tests/test_structure_checks.py's ordinal narrowing. Only a FUNCTION
        # docstring on something other than the decorator's own definition is the hazard: the
        # author wrote a citation where a decorator belonged, and nothing indexes it.
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            if node.name == "source":
                continue
            doc = ast.get_docstring(node)
            if doc and "@source((" in doc:
                in_docstring.append(f"{path.name}:{node.lineno} {node.name}()")
        for node in ast.walk(tree):
            for dec in getattr(node, "decorator_list", []):
                if not (isinstance(dec, ast.Call) and getattr(dec.func, "id", None) == "source"):
                    continue
                for arg in dec.args:
                    try:
                        ref = ast.literal_eval(arg)
                    except (ValueError, SyntaxError):
                        continue
                    if not (isinstance(ref, tuple) and len(ref) == 3):
                        continue
                    text_id, chapter, shlokas = ref
                    yield path, dec.lineno, text_id, chapter, list(shlokas or [])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--astroacharya", type=pathlib.Path, default=DEFAULT_ASTROACHARYA)
    ap.add_argument("--corpus", type=pathlib.Path,
                    default=pathlib.Path(__file__).resolve().parent.parent)
    args = ap.parse_args(argv)

    app = args.astroacharya / "app"
    if not app.is_dir():
        print(f"astroacharya not found at {app} -- pass --astroacharya", file=sys.stderr)
        return 2

    index = corpus_index(args.corpus)
    unreadable: list[str] = []
    in_docstring: list[str] = []
    refs = list(citations(app, unreadable, in_docstring))
    if not refs:
        print(f"parsed 0 @source call sites under {app} -- the reader failed, "
              "this is not a clean result", file=sys.stderr)
        return 2

    missing_text: collections.Counter = collections.Counter()
    missing_verse: list[str] = []
    malformed: list[str] = []
    ok = 0

    for path, line, text_id, chapter, shlokas in refs:
        slug = normalise(text_id)
        where = f"{path.relative_to(args.astroacharya)}:{line}"
        if slug not in index:
            missing_text[f"{text_id} -> {slug}"] += 1
            continue
        bad = [s for s in shlokas if isinstance(s, int) and s < 1]
        if bad:
            malformed.append(f"  {where}  {text_id} ch{chapter} {bad} "
                             f"(a literal like [1-25] evaluates to {bad})")
            continue
        absent = [s for s in shlokas if (str(chapter), str(s)) not in index[slug]]
        if absent:
            missing_verse.append(f"  {where}  {text_id} ch{chapter} verses {absent}")
            continue
        ok += 1

    print(f"@source citations: {len(refs)} call sites across {len(set(r[0] for r in refs))} files")
    print(f"  resolve cleanly     {ok}")
    print(f"  text not in corpus  {sum(missing_text.values())}")
    print(f"  verse not in text   {len(missing_verse)}")
    print(f"  malformed           {len(malformed)}")
    print(f"  files unreadable    {len(unreadable)}")
    print(f"  @source in docstring {len(in_docstring)}  (reads as a citation, indexed by nothing)")

    if missing_text:
        print("\nTEXT NOT IN CORPUS (the citation names a work this corpus does not hold):")
        for name, n in missing_text.most_common():
            print(f"  {n:3}x  {name}")
    if missing_verse:
        print("\nVERSE NOT IN TEXT (the work is held; the cited verse is not in it):")
        print("\n".join(missing_verse))
    if malformed:
        print("\nMALFORMED (valid Python, wrong meaning -- mistyped, not missing):")
        print("\n".join(malformed))

    if unreadable:
        print("\nUNREADABLE (not a clean result -- these files were never checked):")
        for u in unreadable:
            print(f"  {u}")
    if in_docstring:
        print("\n@source INSIDE A DOCSTRING (looks like a citation, is prose):")
        for d in in_docstring:
            print(f"  {d}")

    return 1 if (missing_text or missing_verse or malformed or unreadable) else 0


if __name__ == "__main__":
    raise SystemExit(main())
