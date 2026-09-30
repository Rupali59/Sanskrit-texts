"""The MONGO publication gate — the one that actually feeds the public `/texts` API.

WHY A SECOND GATE TEST. `tests/test_publication_gate.py` proves the POSTGRES gate: a draft never
reaches `published_verse`, and `corpus_api` cannot read the underlying tables. That gate is sound
and it currently protects an empty export -- 0 annotations are `approved`, so it serves nothing.

**The path that serves the public site is the other one, and nothing asserted anything about it.**
`astroacharya/app/api/texts.py` returns the Mongo document wholesale and filters on nothing, so
the only thing between a machine draft and the public API is `seed_texts.py`'s `_normalize_shloka`
-- an allowlist of key names in ANOTHER REPOSITORY. `test_publication_gate.py` names that function
in a comment on line 5 and asserts nothing about it. A comment claiming coverage elsewhere is a
claim about another file (`rule:enforcement-watches-itself`), and this is that claim's test.

WHAT THE GATE ACTUALLY IS, and it is narrower than it looks. `_normalize_shloka` copies by FIELD
NAME. `english_draft` is not in the allowlist, so a draft cannot be published -- **the gate is
structural, not a flag**. Nothing filters on `status`: an `english` value ships whether it was
human-verified or machine-written. So this file asserts the half that holds, and pins the corpus
invariant that keeps the other half harmless.

THE LIVE HAZARD THIS PINS. The allowlist reads
`sh.get("english", sh.get("english_meaning", ""))`. `english_meaning` is on `CLAUDE.md`'s
do-not-add-back list -- a pre-normalisation artifact -- yet it is a live fallback INTO THE SERVED
FIELD. It is currently unreachable only because no verse carries the key. That is a corpus
invariant, not a code guarantee, so it is asserted here: the day a converter re-emits
`english_meaning`, unreviewed text publishes silently and no other check would see it.

DERIVED, NOT RESTATED (`rule:derive-dont-curate`). The key set is parsed out of astroacharya's
real source with `ast`. A hardcoded copy of the 12 keys would pass forever while the function
drifted -- which is precisely how the gotcha describing this gate came to assert four keys when
there were twelve.
"""

from __future__ import annotations

import ast
import json
import pathlib

import pytest

from sanskrit_texts.importer import corpus_files

ROOT = pathlib.Path(__file__).resolve().parent.parent
SEED = ROOT.parent / "astroacharya" / "scripts" / "seed_texts.py"

#: Pre-normalisation artifacts, per `CLAUDE.md` "Do not add back".
BANNED_CORPUS_FIELDS = {
    "source", "header", "book", "english_meaning", "hindi_meaning",
    "source_file", "source_chunk", "is_duplicate",
}


def _fields_normalize_shloka_reads() -> set[str]:
    """Every corpus field name `_normalize_shloka` can copy, read from the real source.

    Returns the literal key of every `sh.get("<key>", ...)` inside the function, including the
    keys of NESTED `.get` calls -- the fallback chain is the whole point, and a reader that only
    saw the outer key would report `english` and miss `english_meaning`.
    """
    tree = ast.parse(SEED.read_text(encoding="utf-8"), filename=str(SEED))
    fn = next(
        (n for n in ast.walk(tree)
         if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == "_normalize_shloka"),
        None,
    )
    if fn is None:
        pytest.fail(f"_normalize_shloka not found in {SEED} -- the gate moved or was renamed; "
                    "this is not a clean result")
    keys: set[str] = set()
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Attribute) and f.attr == "get" and isinstance(f.value, ast.Name) \
                and f.value.id == "sh" and node.args:
            k = node.args[0]
            if isinstance(k, ast.Constant) and isinstance(k.value, str):
                keys.add(k.value)
    return keys


requires_astroacharya = pytest.mark.skipif(
    not SEED.exists(),
    # Absence must be attributable -- a skip that reads as a pass is the failure this guards.
    reason=f"astroacharya not checked out at {SEED} -- the Mongo gate was NOT verified",
)


@requires_astroacharya
def test_the_allowlist_cannot_copy_a_draft_field():
    """No `*_draft` key is readable by the seeder. This is the whole draft gate."""
    keys = _fields_normalize_shloka_reads()
    assert len(keys) >= 5, (
        f"only {len(keys)} corpus fields parsed out of _normalize_shloka -- the AST reader has "
        "gone blind, it has not found a narrow allowlist"
    )
    drafts = {k for k in keys if k.endswith("_draft")}
    assert not drafts, (
        f"_normalize_shloka can now copy {sorted(drafts)} into Mongo. `app/api/texts.py` returns "
        "the document wholesale, so this publishes machine-drafted translation to the public "
        "/texts API. This is the edit G50 exists to prevent -- revert it."
    )


@requires_astroacharya
def test_banned_artifact_fields_are_unreachable_from_the_corpus():
    """`english_meaning` is a live fallback into the served field; no verse may carry it.

    Two ways this goes green and only one is good: the fallback is removed from astroacharya, or
    the corpus carries none of the keys. Both are checked, so removing the fallback does not
    silently retire the corpus invariant and vice versa.
    """
    reachable_banned = _fields_normalize_shloka_reads() & BANNED_CORPUS_FIELDS

    walked = 0
    carriers: dict[str, int] = {}
    for path in corpus_files(ROOT):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(doc, dict) or "chapters" not in doc:
            continue
        for ch in doc["chapters"]:
            for sh in ch.get("shlokas") or []:
                walked += 1
                for banned in BANNED_CORPUS_FIELDS:
                    if banned in sh:
                        carriers[banned] = carriers.get(banned, 0) + 1

    assert walked > 50_000, f"only {walked} verses walked -- the scan has gone blind"

    # The dangerous intersection: a banned field the seeder would COPY, present in the corpus.
    live = {b: n for b, n in carriers.items() if b in reachable_banned}
    assert not live, (
        f"{live} -- these verses carry a banned field that _normalize_shloka copies straight into "
        f"the served `english`/`hindi`. Unreviewed text would publish. Reachable banned fields in "
        f"the seeder right now: {sorted(reachable_banned)}"
    )
    assert not carriers, (
        f"pre-normalisation artifacts are back in the corpus: {carriers}. Not publishable today, "
        "but CLAUDE.md forbids them and the seeder's fallback chain makes two of them one edit away."
    )


@requires_astroacharya
def test_the_gate_is_structural_and_status_is_not_a_filter():
    """Pin the shape of the gate, so a reader is not misled about what protects them.

    `status` IS copied and nothing filters on it, so an unverified `english` publishes. That is the
    known gap; it is asserted rather than described so that closing it is a visible, failing edit
    here rather than a silent change in another repo.
    """
    keys = _fields_normalize_shloka_reads()
    assert "status" in keys, "status is no longer carried -- the seeder's shape changed"
    assert {"english", "hindi", "text"} <= keys, (
        f"the served fields are no longer read by name: {sorted(keys)}"
    )
    src = SEED.read_text(encoding="utf-8")
    fn_src = src[src.index("def _normalize_shloka"):]
    fn_src = fn_src[:fn_src.index("\nasync def ") if "\nasync def " in fn_src else len(fn_src)]
    assert "approved" not in fn_src, (
        "_normalize_shloka now mentions `approved` -- if a state filter was added, this test "
        "should be rewritten to assert it, not to record its absence."
    )
