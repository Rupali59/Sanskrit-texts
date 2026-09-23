"""Read-only summaries of the corpus, from either source it lives in.

WHY THIS EXISTS. `check_inventory.py`, `tag_features.py` and `spot_check.py` all `json.load`
the corpus directly, and none of them imports `sanskrit_texts` -- even though the store exists
and is imported (STATE.md, 2026-09-16: 97,724 verses landed). A capability nobody invokes is
indistinguishable from one that was never built (`rule:enforcement-watches-itself` §2). This
is the first consumer, named in the plan's §5.

ONE SHAPE, TWO SOURCES. `check_inventory.py` already defines the shape a caller needs -- one
dict per `text_id` with `{'ch','sh','tr','pct','dir','cat','dupes','titles','authority'}`. That
shape is not renegotiated here. `load_corpus_from_json` is that function, moved unmodified so
`--source=json` behaves exactly as before (verified by diffing the script's output). Both
`load_corpus_from_db` and `load_corpus` (the dispatcher) return the same shape.

THE DSN DEFAULT IS THE WHOLE POINT, NOT A DETAIL. `load_corpus_from_db` connects with
`CORPUS_API_DSN` by default and NEVER reads `CORPUS_OWNER_DSN` from the environment on its
own -- the entire publication gate (docs/DATABASE.md) rests on no consumer ever holding the
owner DSN, and a reader that defaulted to owner would be the first place that promise quietly
broke. An owner DSN reaches this module only if a caller passes one explicitly via `dsn=`.

WHY JSON STAYS THE DEFAULT SOURCE, NOT DB. `check_inventory.py` is the gate that must pass
BEFORE the importer runs (docs/DATABASE.md: `make hello` precedes `make import`). A reader
that could only read the database would make the first command in that runbook impossible to
run against an empty store -- so `load_corpus(source=...)` defaults to `"json"`.

SQLALCHEMY IS IMPORTED LAZILY, INSIDE `load_corpus_from_db`, NOT AT MODULE LEVEL. This module
is imported by `check_inventory.py`, which today runs under bare system `python3` with no
dependencies at all. A module-level `import sqlalchemy` would break that for every caller,
including the JSON-only default path, just because the *db* path exists. The JSON half of
this module is stdlib-only for the same reason `check_inventory.py` was.

WHAT THE API-SOURCED SUMMARY CANNOT SEE, AND WHY THAT IS THE GATE WORKING, NOT A GAP HERE.
The API role holds `SELECT` on exactly two views -- `published_text` and `published_verse`
(`migrations/versions/0001_corpus_schema_and_gate.py`) -- and nothing else:

  * `published_verse` LEFT JOINs `annotation ... AND state = 'approved'`. Every annotation in
    the store today is `draft` (STATE.md 2026-09-16: 0 approved), so every verse's
    kind/lang/value come back NULL through the API DSN. `tr`/`pct` therefore measure REVIEW
    STATE (how much has a named human approved), not ARRIVAL STATE (the JSON `status` field
    check_inventory's json source counts). They read 0 today, correctly -- nothing has been
    approved yet, and the view does not let a consumer see otherwise. Comparing this `pct`
    against the JSON source's `pct` would be comparing unlike things (`rule:discernment-checks`
    §5); callers must not do it.
  * `published_verse` exposes a verse's own (leaf) section, not its ancestors --
    `section.parent_id` is not a granted column. `section` is a RAGGED tree (docs/DATABASE.md):
    a verse under a multi-level text sits under a pada/khanda below its chapter, so which
    ROOT chapter it belongs to is not recoverable through the API surface alone. `ch` is
    reported as `None` here rather than guessed -- a plausible-looking wrong chapter count is
    the "check that cannot fail" failure mode (`rule:discernment-checks` §1), worse than an
    honest "not observable this way".
  * `dir` (the source file's directory) and `dupes` (labels the importer refused under
    `uq_verse_label_in_section`) are JSON-file facts with no database column: `text` carries
    no path, and a refused duplicate is never stored, not merely deduplicated. Both come back
    `None` from the db source for the same reason as `ch`.

So the two sources are NOT expected to agree field-for-field. What both sources can see in
full, and must agree on, is which texts exist and how many verses each one holds --
anything in `sanskrit_texts/exclusions.py` aside, which the db source omits by design and the
json source includes. `tests/test_reader.py` asserts exactly that overlap, not the fields
neither source can supply. (That set held four texts from 2026-09-16 and is EMPTY as of
2026-09-23: all four left the tree, so the two sources now agree outright. The allowance stays
because the next exclusion will need it.)

VERSE-LEVEL, FOR THE SCRIPTS THAT EDIT OR SAMPLE WHOLE VERSES, NOT COUNTS. `tag_features.py`
and `spot_check.py` each need a full `{'chapters': [...]}` document for one `text_id` -- the
former to mutate `sh['tags']` in place and write the file back, the latter to sample shlokas
for review -- and until now each hand-rolled its own walk to get one: `tag_features.py` called
`entity_roots.py`'s `load_text`, and `spot_check.py` skipped the walk entirely and hardcoded
the path to BPHS. Three walks (this module's summary one, `entity_roots.py`'s, and
`importer.py`'s own `load_corpus`) already disagreed slightly on what to skip -- `load_text`
checked only the FIRST path component for a dot-prefix, this module's walk checks every
component -- which is exactly the "capability nobody invokes is indistinguishable from one
never built" shape one level down: not an unused capability, but four DIFFERENT
implementations of the same one, free to drift apart silently. `load_text_from_json` is the
one shape both scripts now share; it reuses this module's own skip rule (`docs/`, any
dot-directory) rather than `entity_roots.py`'s narrower one, since a rule that skips a
superset of what the narrower one did cannot make either script see a NEW text -- only ever
fewer of the same false candidates (dot-directories, which hold no real corpus text either way).

WHY A BROKEN FILE ELSEWHERE DOES NOT ABORT THE SEARCH, UNLIKE `load_corpus_from_json`.
`load_corpus_from_json` exists to summarise -- and implicitly validate -- EVERY text, so a file
that fails to parse is exactly the fact it exists to surface, and it raises. `load_text_from_json`
is a targeted lookup for ONE text_id; a different file being transiently unparseable (this repo
is actively being rewritten by concurrent digitisation and tagging passes -- see STATE.md) is not
a fact about the wanted text and must not crash a script that never asked about the broken one.
This matches `entity_roots.py`'s superseded `load_text`, which already skipped unparseable files
while walking -- so `tag_features.py`'s tolerance for a broken sibling file is unchanged by this
migration, and `spot_check.py` gains the same tolerance it never needed before (it read one
hardcoded path) now that it walks too. If the WANTED file itself is the one that is transiently
broken, the walk simply does not find it and reports `TextNotFoundError` -- indistinguishable
from "does not exist", which is the same ambiguity `entity_roots.py`'s `load_text` already had.

WHY IT RETURNS THE RAW DICT, NOT A TYPED SHAPE. `tag_features.py` re-serialises exactly what
it read (`json.dumps(doc, ...)`) after mutating `sh['tags']` in place, so the function must
hand back the same nested `dict`/`list` structure `json.loads` produced -- wrapping it in a
typed object would mean unwrapping it again before the write, which is a second place for the
round-trip to silently lose a field.

WHY THIS DOES NOT CONSULT `sanskrit_texts/exclusions.py`. Neither script checks it today --
`tag_features.py` operates on whatever `--text` names (default `bphs`) and `spot_check.py`
always reads `bphs`; neither has ever refused an excluded text_id. Adding that check here
would change which texts these two scripts can see, silently, which the brief for this
migration explicitly rules out. If a caller ever needs the check, it belongs at the call
site that decided to exclude something, the way `importer.run` does it -- not buried in a
loader two other callers use without asking for it.
"""

from __future__ import annotations

import collections
import json
import os
from collections.abc import Iterable
from pathlib import Path
from typing import Any

Summary = dict[str, Any]  # {'ch','sh','tr','pct','dir','cat','dupes','titles','authority'}
Doc = dict[str, Any]  # a full corpus text: {'text_id', 'title_sa', ..., 'chapters': [...]}

SOURCES = ("json", "db")


def derive_text_status(verse_statuses: Iterable[str | None]) -> str:
    """The TEXT-level `status`, derived from its verses -- never asserted independently.

    28 texts carry a text-level `status`. A translation run stamped all 28 `translated` on
    2026-09-16; after the quarantine that evening 17 of them were false (Manusmrti 0/2,684,
    Rgveda 0/10,470). A cached summary that can disagree with its source is only safe if
    something re-derives it, so the value is recomputed from this function and
    `tests/test_reader.py` fails if any file's stored value differs from it.

      every verse `translated`                  -> translated
      else any verse `translated` or `partial`  -> partial
      else any verse `drafted`                  -> drafted
      else                                      -> untranslated

    `drafted` outranks `untranslated` because it is the more informative claim: machine text
    exists and awaits review. An empty text is `untranslated`, not `translated` -- `all()` over
    nothing is True, and a text with no verses has translated nothing.
    """
    seen = collections.Counter(verse_statuses)
    total = sum(seen.values())
    if total and seen["translated"] == total:
        return "translated"
    if seen["translated"] or seen["partial"]:
        return "partial"
    if seen["drafted"]:
        return "drafted"
    return "untranslated"


class TextNotFoundError(LookupError):
    """No corpus JSON under `root` declares this text_id -- including when `root` holds no
    corpus at all (an empty directory walks to zero matches exactly like a populated one that
    simply lacks this text_id; both raise this, never a bare `None`/`{}`, per
    `rule:discernment-checks` §2 -- absence must be attributable).

    Deliberately NOT `SystemExit`. A missing text_id is an ordinary, expected outcome that
    `tag_features.py` and `spot_check.py` each already promise to handle with their own exit
    code (2, "could not run" -- see their own docstrings' "Exit codes" sections), so it must
    be catchable, not fatal-by-construction.
    """


def load_text_from_json(text_id: str, *, root: Path | None = None) -> tuple[Doc, Path]:
    """The verse-level counterpart to `load_corpus_from_json` below -- the full document for
    ONE text (every chapter, every shloka), not a per-text summary. See the module docstring's
    "VERSE-LEVEL" section for why this exists, why it returns a raw dict, and why -- unlike
    `load_corpus_from_json` -- an unrelated file that fails to parse is skipped rather than
    fatal: this is a targeted lookup, not a corpus-wide integrity check, and the corpus is
    edited concurrently by other passes (STATE.md).

    Returns `(doc, rel)` where `rel` is the matched file's path relative to `root`, mirroring
    `entity_roots.py`'s now-superseded `load_text` so its one remaining caller (`tag_features.py`,
    which needs `rel` to write the file back) did not have to change how it uses the result.

    Raises `TextNotFoundError` if no file declares this text_id by the time the walk is
    exhausted -- including when the wanted file exists but was transiently unparseable (the
    same ambiguity `entity_roots.py`'s `load_text` already had) and when `root` holds no JSON
    at all.
    """
    base = root if root is not None else Path(".")
    for p in sorted(base.rglob("*.json")):
        rel = p.relative_to(base)
        # Same skip rule as `load_corpus_from_json`, not `entity_roots.py`'s narrower one --
        # see the module docstring's "VERSE-LEVEL" section for why the difference is safe.
        if rel.parts[0] == "docs" or any(part.startswith(".") for part in rel.parts):
            continue
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Unlike `load_corpus_from_json`: a file this lookup was never asked about failing
            # to parse -- possibly mid-write by a concurrent pass -- is not evidence about the
            # TEXT_ID being searched for. See the module docstring's "WHY A BROKEN FILE
            # ELSEWHERE" section.
            continue
        if doc.get("text_id") == text_id:
            return doc, rel
    raise TextNotFoundError(f"no text with text_id {text_id!r} under {base}")


# Fields the db source cannot populate and reports as None, with the reason given in the
# module docstring above. Kept as a named set (not scattered literals) so a caller -- or a
# test -- can ask "which fields does this source promise?" instead of rediscovering it.
DB_UNAVAILABLE_FIELDS = ("ch", "dir", "dupes")


def load_corpus_from_json(root: Path) -> dict[str, Summary]:
    """Walk the corpus JSON and summarise each text. Moved from `check_inventory.py`
    unchanged -- this IS the function that script has always run; only its address changed."""
    out: dict[str, Summary] = {}
    for p in sorted(root.rglob("*.json")):
        rel = p.relative_to(root)
        # `docs/` is prose; a dot-directory is tooling config (.claude/, .cursor/) and an
        # unparseable settings.json there must not read as a corpus failure.
        if rel.parts[0] == "docs" or any(part.startswith(".") for part in rel.parts):
            continue
        try:
            j = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            raise SystemExit(f"could not run: {rel} is not readable JSON ({e})") from e
        tid = j.get("text_id")
        if not tid:
            continue
        chs = j.get("chapters") or []
        n = sum(len(c.get("shlokas", [])) for c in chs)
        # Dedupe loss: astroacharya's seed_texts.py keys on (chapter, shloka), later wins, and
        # only LOGS the collision -- so a duplicate key is a shloka that never reaches Mongo
        # (G8). This counts what is present, not what is ingestible.
        keys: collections.Counter = collections.Counter()
        for c in chs:
            for sh in c.get("shlokas", []):
                keys[(c.get("number"), sh.get("number"))] += 1
        dupes = sum(v - 1 for v in keys.values() if v > 1)
        tr = sum(1 for c in chs for s in c.get("shlokas", []) if s.get("status") == "translated")
        if tid in out:
            raise SystemExit(f"could not run: text_id {tid!r} declared twice")
        out[tid] = {
            "ch": len(chs),
            "sh": n,
            "tr": tr,
            "pct": round(100 * tr / n) if n else 0,
            "dir": str(rel.parent),
            "cat": j.get("category"),
            "dupes": dupes,
            "titles": f"{j.get('title_en', '')} {j.get('title_sa', '')}",
            "authority": (j.get("structure") or {}).get("count_authority"),
        }
    return out


def load_corpus_from_db(dsn: str | None = None) -> dict[str, Summary]:
    """Summarise the corpus through the published surface -- the same surface any other
    consumer gets. `dsn` defaults to `CORPUS_API_DSN`; `CORPUS_OWNER_DSN` is read only if a
    caller passes it explicitly (see the module docstring's "DSN default" section)."""
    import sqlalchemy as sa  # lazy: see module docstring -- keeps the json path dependency-free

    dsn = dsn or os.environ.get("CORPUS_API_DSN")
    if not dsn:
        raise RuntimeError(
            "no DSN: pass dsn=, or set CORPUS_API_DSN. Never CORPUS_OWNER_DSN implicitly -- "
            "see sanskrit_texts/reader.py's module docstring."
        )
    engine = sa.create_engine(dsn, future=True)
    with engine.connect() as conn:
        texts = (
            conn.execute(
                sa.text("SELECT id, title_sa, title_en, category, structure FROM published_text")
            )
            .mappings()
            .all()
        )
        # Absence must be attributable (`rule:discernment-checks` §2): an empty store and a
        # wrong/unreachable DSN both look like "0 rows" to the caller unless this says which.
        if not texts:
            raise RuntimeError(
                f"published_text returned 0 rows via {dsn.split('@')[-1]!r} -- the store is "
                "empty or the connection is wrong, not merely lacking approved content. "
                "Run `make import` (owner DSN) first, or check the DSN."
            )
        verse_rows = (
            conn.execute(
                sa.text("SELECT text_id, verse_id, kind, lang, value FROM published_verse")
            )
            .mappings()
            .all()
        )

    all_verses: dict[str, set[int]] = collections.defaultdict(set)
    translated_verses: dict[str, set[int]] = collections.defaultdict(set)
    for r in verse_rows:
        all_verses[r["text_id"]].add(r["verse_id"])
        # An approved English translation. published_verse LEFT JOINs annotation on
        # state='approved', so this is empty for every verse today (0 approved) -- correctly:
        # the view does not let an API consumer see anything else.
        if r["kind"] == "translation" and r["lang"] == "en" and r["value"] is not None:
            translated_verses[r["text_id"]].add(r["verse_id"])

    out: dict[str, Summary] = {}
    for t in texts:
        tid = t["id"]
        sh = len(all_verses.get(tid, ()))
        tr = len(translated_verses.get(tid, ()))
        out[tid] = {
            "ch": None,  # not observable through the API surface -- see module docstring
            "sh": sh,
            "tr": tr,
            "pct": round(100 * tr / sh) if sh else 0,
            "dir": None,  # no filesystem path in the database
            "cat": t["category"],
            "dupes": None,  # refused at import (uq_verse_label_in_section), never stored
            "titles": f"{t['title_en'] or ''} {t['title_sa'] or ''}",
            "authority": (t["structure"] or {}).get("count_authority"),
        }
    return out


def load_corpus(
    source: str = "json", *, root: Path | None = None, dsn: str | None = None
) -> dict[str, Summary]:
    """Dispatch to the requested source. Defaults to json -- see the module docstring's
    "WHY JSON STAYS THE DEFAULT" section for why that default is load-bearing, not arbitrary."""
    if source == "json":
        return load_corpus_from_json(root if root is not None else Path("."))
    if source == "db":
        return load_corpus_from_db(dsn)
    raise ValueError(f"unknown source {source!r}: expected one of {SOURCES}")
