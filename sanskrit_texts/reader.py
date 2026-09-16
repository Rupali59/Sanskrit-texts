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
`sanskrit_texts/exclusions.py`'s four texts aside, which the db source omits by design and the
json source includes. `tests/test_reader.py` asserts exactly that overlap, not the fields
neither source can supply.
"""

from __future__ import annotations

import collections
import json
import os
from pathlib import Path
from typing import Any

Summary = dict[str, Any]  # {'ch','sh','tr','pct','dir','cat','dupes','titles','authority'}

SOURCES = ("json", "db")

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
