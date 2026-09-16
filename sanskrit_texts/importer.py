"""Import the corpus JSON into the modelled store.

THE IMPORTER IS DUMB ON PURPOSE. It reads each text's `structure` declaration and never
infers. Numbering is a per-text property, and per-text properties already have a home -- the
`structure` block, which carries `levels` and `shloka_number_format` for exactly this. The
alternative (one global rule, or a `levels.py` of per-text special cases) was tried in the
design and rejected: it makes code and data compete to describe the same fact, and the corpus
holds 12 distinct level shapes across 66 texts.

FOUR RULES THAT ARE NOT NEGOTIABLE, each paid for:

1. **`levels` is the MAXIMUM depth, not a uniform one.** Caraka's Cikitsasthana subdivides
   adhyayas 1-2 into padas and leaves the other 28 alone, so a label with fewer components
   means that branch is not subdivided -- it is not an error. A check that assumed uniform
   depth accused ~20% of the corpus before the check itself turned out to be wrong
   (DECISIONS 2026-09-15 D4).
2. **A depth-carrying label with no declaration is REFUSED, never guessed.** Exactly one text
   was in that state (`apastamba_dharma_sutra`, 1,315 dotted labels) and the fix was to write
   its declaration, not to teach the importer to parse dots.
3. **Array order is authoritative for `position`.** It is what the source edition emitted, and
   it disagrees with numeric label order in 17 chapters across three texts. Those are a
   recorded reconciliation finding, not a bug to repair at read time.
4. **Everything lands `state='draft'`.** Nothing imports as `approved`, because no row has a
   named reviewer. `status` is preserved on the verse as the ARRIVAL field and is NOT an
   editorial claim (DECISIONS 2026-09-16).

DRY-RUN RUNS THE REAL IMPORT. It executes the same INSERTs against the same constraints inside
a transaction it never commits, wrapping each text in a SAVEPOINT so one text's violation does
not abort the rest. A dry-run that validated in Python instead would be a second oracle, free
to disagree with the database -- which is the shape `rule:safety-flag-needs-a-test` records
three paid instances of.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import pathlib
import sys
from typing import Any, Iterable

import sqlalchemy as sa
from sqlalchemy.exc import IntegrityError

from sanskrit_texts.exclusions import EXCLUDED_TEXTS
from sanskrit_texts.models import Annotation, AnnotationRevision, Verse

REPO = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {"docs", ".venv", ".venv-corpus", "migrations", "node_modules", "venv", ".git"}

# Used when a text declares no `levels` AND every one of its labels is single-component.
# Explicit, so "we defaulted" is a recorded fact rather than an invisible assumption.
DEFAULT_LEVELS = ["chapter", "verse"]

LANGS = {"english": "en", "hindi": "hi"}

# D10: the directory's middle level is a classification axis, and which axis depends on the
# top level. Derived from the PATH, which is where the corpus already records it -- not from a
# hand-kept table that would drift from the tree the first time a text moved.
FACET_BY_TOP = {
    "Hora": "school",          # Parashari 14 · Jaimini 2 · Nadi 1
    "Upanishad": "shakha",     # krishna-yajurveda 7 · shukla-yajurveda 5 · atharvaveda 3 · ...
    "Upaveda": "discipline",   # Ayurveda 5 · Sthapatyaveda 2 · Dhanurveda 1
    "Veda": "veda",            # one per Veda
    "Vedanga-Jyotisha": "recension",
}

# D11: Siddhanta Siromani is one work in four parts sharing a directory -- the only real case
# in 66 texts, so it is named rather than inferred from a directory-sharing heuristic that
# would also catch unrelated neighbours.
PART_OF = {
    "lilavati": "siddhanta_shiromani",
    "bijaganita": "siddhanta_shiromani",
    "grahaganita": "siddhanta_shiromani",
    "goladhyaya": "siddhanta_shiromani",
}
PARENT_WORKS = {"siddhanta_shiromani": ("सिद्धान्तशिरोमणिः", "Siddhanta Shiromani", "siddhanta")}


@dataclasses.dataclass(frozen=True)
class Violation:
    text_id: str
    where: str
    kind: str
    detail: str

    def __str__(self) -> str:
        return f"{self.text_id:<28} {self.where:<16} {self.kind:<22} {self.detail}"


@dataclasses.dataclass
class Result:
    texts: int = 0
    sections: int = 0
    verses: int = 0
    annotations: int = 0
    revisions: int = 0
    facets: int = 0
    skipped: list[str] = dataclasses.field(default_factory=list)
    violations: list[Violation] = dataclasses.field(default_factory=list)


def corpus_files(root: pathlib.Path = REPO) -> Iterable[pathlib.Path]:
    for path in sorted(root.rglob("*.json")):
        if set(path.relative_to(root).parts) & SKIP_DIRS:
            continue
        yield path


def load_corpus(only: set[str] | None = None) -> list[tuple[pathlib.Path, dict[str, Any]]]:
    out = []
    # When a caller names the texts it wants, a SUBSTRING test on the raw bytes decides
    # membership before the expensive parse. The corpus is ~200 MB across ~100 files and
    # `json.loads` on all of it to keep 5 texts took 114s cold -- the round-trip test's whole
    # runtime. Reading is unavoidable; parsing is not.
    # Match the QUOTED SLUG alone, not `"text_id": "slug"`: the latter assumes a space after
    # the colon, so a minified file would be skipped silently -- and a false negative here
    # means a text vanishes from the import with no error. A false positive only costs one
    # parse, which the `text_id` check below then rejects.
    wanted = {f'"{t}"' for t in only} if only is not None else None
    for path in corpus_files():
        try:
            raw = path.read_text(encoding="utf-8")
            if wanted is not None and not any(w in raw for w in wanted):
                continue
            doc = json.loads(raw)
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(doc, dict) or "text_id" not in doc or "chapters" not in doc:
            continue
        if only is not None and doc["text_id"] not in only:
            continue
        doc["_sha"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        doc["_path"] = path
        out.append((path, doc))
    return out


def resolve_levels(doc: dict[str, Any]) -> tuple[list[str] | None, Violation | None]:
    """The declaration, or the explicit default -- or a refusal, never a guess."""
    tid = doc["text_id"]
    declared = (doc.get("structure") or {}).get("levels")
    if declared:
        return list(declared), None
    deepest = max(
        (str(s.get("number")).count(".") + 1
         for c in doc["chapters"] for s in c.get("shlokas", [])),
        default=1,
    )
    if deepest > 1:
        return None, Violation(
            tid, "structure", "undeclared-depth",
            f"labels carry {deepest} components but `structure.levels` is absent. "
            f"Declare the level names in the JSON; the importer does not infer them.",
        )
    return list(DEFAULT_LEVELS), None


def _components(label: str) -> list[str]:
    return str(label).split(".")


def import_text(conn: sa.Connection, doc: dict[str, Any], result: Result,
                *, enumerate_all: bool = False) -> None:
    """Insert one text. Raises IntegrityError, which the caller turns into a Violation."""
    tid = doc["text_id"]
    levels, bad = resolve_levels(doc)
    if bad is not None:
        result.violations.append(bad)
        result.skipped.append(tid)
        return

    conn.execute(
        sa.text(
            "INSERT INTO text (id, title_sa, title_en, category, structure, source_sha)"
            " VALUES (:id, :sa, :en, :cat, CAST(:st AS jsonb), :sha)"
        ),
        {
            "id": tid, "sa": doc.get("title_sa"), "en": doc.get("title_en"),
            "cat": doc.get("category"),
            "st": json.dumps(doc.get("structure"), ensure_ascii=False)
            if doc.get("structure") is not None else None,
            "sha": doc["_sha"],
        },
    )
    result.texts += 1

    # D10: one facet row per text, from the path. 52 of 66 carry one; the 14 that do not are
    # the four Siromani parts (handled by part_of) and 10 genuinely standalone works.
    rel = doc["_path"].relative_to(REPO).parts
    kind = FACET_BY_TOP.get(rel[0]) if len(rel) > 2 else None
    if kind:
        conn.execute(
            sa.text("INSERT INTO text_facet (text_id, kind, value) VALUES (:t, :k, :v)"),
            {"t": tid, "k": kind, "v": rel[1]},
        )
        result.facets += 1

    verse_rows: list[dict[str, Any]] = []
    ann_rows: list[dict[str, Any]] = []

    for ch_pos, chapter in enumerate(doc["chapters"], start=1):
        chapter_label = str(chapter.get("number"))
        root_id = conn.execute(
            sa.text(
                "INSERT INTO section (text_id, parent_id, depth, level_name, label, title,"
                " title_en, position) VALUES (:t, NULL, 1, :ln, :lb, :ti, :te, :p)"
                " RETURNING id"
            ),
            {"t": tid, "ln": levels[0], "lb": chapter_label,
             "ti": chapter.get("title"), "te": chapter.get("title_en"), "p": ch_pos},
        ).scalar_one()
        result.sections += 1

        # Intermediate sections are created lazily, keyed by their label path under this
        # chapter. A label shorter than max depth simply creates fewer of them -- rule 1.
        mids: dict[tuple[str, ...], int] = {}

        for v_pos, shloka in enumerate(doc["chapters"][ch_pos - 1].get("shlokas", []), start=1):
            comps = _components(shloka.get("number"))
            # levels = [chapter, ..., verse]; everything between is a section level.
            mid_names = levels[1:-1]
            mid_vals = comps[:-1][: len(mid_names)]
            parent_id, depth = root_id, 1
            for i, val in enumerate(mid_vals):
                key = tuple(mid_vals[: i + 1])
                if key not in mids:
                    depth_here = 2 + i
                    mids[key] = conn.execute(
                        sa.text(
                            "INSERT INTO section (text_id, parent_id, depth, level_name,"
                            " label, position) VALUES (:t, :pa, :d, :ln, :lb, :p)"
                            " RETURNING id"
                        ),
                        {"t": tid, "pa": parent_id, "d": depth_here,
                         "ln": mid_names[i], "lb": val, "p": len(mids) + 1},
                    ).scalar_one()
                    result.sections += 1
                parent_id, depth = mids[key], 2 + i

            verse_rows.append({
                "section_id": parent_id,
                "number_label": comps[-1],
                "position": v_pos,
                "devanagari": shloka.get("text") or "",
                "ref": shloka.get("ref"),
                "meter": shloka.get("meter"),
                "status": shloka.get("status"),
                "number_is_str": isinstance(shloka.get("number"), str),
                "_shloka": shloka,
                "_chapter": chapter_label,
            })

    # Verses in one statement per text; RETURNING gives the ids back in insertion order.
    if verse_rows and enumerate_all:
        # SLOW PATH, entered only for a text that already failed. One verse per savepoint, so
        # every violating label is named instead of just the first -- the plan promises "all 70
        # at once", and a bulk insert can only ever report one. It uses the SAME constraint as
        # the fast path; a Python-side duplicate check here would be a second oracle, free to
        # disagree with the database (rule:safety-flag-needs-a-test).
        ids: list[int] = []
        for row in verse_rows:
            payload1 = {k: v for k, v in row.items() if not k.startswith("_")}
            sp = conn.begin_nested()
            try:
                vid = conn.execute(
                    sa.insert(Verse.__table__).returning(Verse.__table__.c.id), payload1
                ).scalar_one()
                sp.commit()
                ids.append(vid)
            except IntegrityError as exc:
                sp.rollback()
                result.violations.append(Violation(
                    tid, f"{row['_chapter']}.{row['number_label']}", "duplicate-verse-label",
                    f"a verse with this label already exists in this section; the seeder's "
                    f"(chapter, shloka) dedupe drops it silently today (G8). "
                    f"{str(getattr(exc, 'orig', exc)).split(chr(10))[0][:80]}",
                ))
                ids.append(None)
        result.verses += sum(1 for i in ids if i is not None)
        for vid, row in zip(ids, verse_rows):
            if vid is not None:
                ann_rows.extend(_annotations_for(vid, row["_shloka"]))
    elif verse_rows:
        payload = [{k: v for k, v in r.items() if not k.startswith("_")} for r in verse_rows]
        # insert().returning(), NOT text(): only the Core construct triggers SQLAlchemy's
        # insertmanyvalues, which is what makes RETURNING work for an executemany. A raw
        # text() here raises ResourceClosedError -- the statement runs, the ids are lost.
        ids = conn.execute(
            sa.insert(Verse.__table__).returning(Verse.__table__.c.id), payload
        ).scalars().all()
        result.verses += len(ids)

        for vid, row in zip(ids, verse_rows):
            ann_rows.extend(_annotations_for(vid, row["_shloka"]))

    if ann_rows:
        aids = conn.execute(
            sa.insert(Annotation.__table__).returning(Annotation.__table__.c.id),
            [{k: v for k, v in dict(r, state="draft").items() if not k.startswith("_")}
             for r in ann_rows],
        ).scalars().all()
        result.annotations += len(aids)
        # One baseline revision per annotation: provenance starts at import, not at first edit.
        conn.execute(
            sa.insert(AnnotationRevision.__table__),
            # The NOTE records which source field the value came from -- a FACT. It does not
            # claim who wrote it: a value sitting in `english` may be curated or may be a
            # promoted machine draft, and the corpus does not record which. Asserting `human`
            # here would manufacture exactly the provenance UC1 withdrew D9 for.
            [{"annotation_id": a, "value": r["value"], "state": "draft", "method": "machine",
              "note": f"baseline at corpus import, from the {r['_src']!r} field"}
             for a, r in zip(aids, ann_rows)],
        )
        result.revisions += len(aids)


def _annotations_for(verse_id: int, shloka: dict[str, Any]) -> list[dict[str, Any]]:
    """Every annotation-bearing key on one verse.

    `english` and `english_draft` can BOTH be populated -- 2,369 verses carry a draft beside a
    served value -- so they are two rows, not a choice. Both land `draft`; which one a reviewer
    later approves is an editorial act, not an import-time inference.
    """
    out: list[dict[str, Any]] = []
    for field, lang in LANGS.items():
        for key in (field, f"{field}_draft"):
            raw = shloka.get(key) or ""
            # STRIP ONLY TO TEST EMPTINESS, never to store. Stripping the stored value silently
            # rewrote 138 translations whose leading space is committed data -- Chandogya
            # 8.12.6 holds `" देवगण ब्रह्मलोक..."` and the round-trip turned it into
            # `"देवगण..."`. An importer that tidies its input cannot prove it lost nothing.
            value = raw if raw.strip() else ""
            if value:
                out.append({"verse_id": verse_id, "kind": "translation", "lang": lang,
                            "value": value, "position": None, "source_field": key,
                            "_src": key})
    # ONE counter across BOTH lists. Numbering each from 1 made `tags[0]` and `tags_draft[0]`
    # both position 1 on the same verse -- and since UC1 lands everything `draft`, the two
    # rows are otherwise identical, so the orders interleaved irrecoverably. Observed on a
    # verse holding 14 tags, where positions 1-3 each appeared twice.
    pos = 0
    for key in ("tags", "tags_draft"):
        for tag in shloka.get(key) or []:
            tag = str(tag) if str(tag).strip() else ""
            if tag:
                pos += 1
                out.append({"verse_id": verse_id, "kind": "tag", "lang": None,
                            "value": tag, "position": pos, "source_field": key,
                            "_src": key})
    return out


def run(dsn: str, *, only: set[str] | None, dry_run: bool,
        allow_partial: bool = False) -> Result:
    result = Result()
    engine = sa.create_engine(dsn, future=True)
    docs = load_corpus(only)
    for _, doc in docs:
        if doc["text_id"] in EXCLUDED_TEXTS:
            result.skipped.append(doc["text_id"])
    docs = [(p, d) for p, d in docs if d["text_id"] not in EXCLUDED_TEXTS]

    with engine.connect() as conn:
        outer = conn.begin()
        try:
            # D11: the parent work owns no verses and exists in no file, so the importer
            # creates it. Only when one of its parts is actually in scope.
            for parent, (sa_t, en_t, cat) in PARENT_WORKS.items():
                if any(PART_OF.get(d["text_id"]) == parent for _, d in docs):
                    conn.execute(
                        sa.text("INSERT INTO text (id, title_sa, title_en, category)"
                                " VALUES (:i, :s, :e, :c)"),
                        {"i": parent, "s": sa_t, "e": en_t, "c": cat},
                    )
                    result.texts += 1
            for _, doc in docs:
                # Snapshot the counters: a rolled-back attempt must not leave its tallies
                # behind, or the retry double-counts the text and its sections. Reported 69
                # texts and 3,878 sections for a 66-text corpus before this.
                snapshot = (result.texts, result.sections, result.verses,
                            result.annotations, result.revisions)
                sp = conn.begin_nested()
                try:
                    import_text(conn, doc, result)
                    sp.commit()
                except IntegrityError:
                    # The bulk insert aborts on its FIRST violation, so re-run this one text
                    # verse-by-verse to name every offending label. Only failing texts pay it.
                    sp.rollback()
                    (result.texts, result.sections, result.verses,
                     result.annotations, result.revisions) = snapshot
                    before = len(result.violations)
                    sp2 = conn.begin_nested()
                    try:
                        import_text(conn, doc, result, enumerate_all=True)
                        sp2.commit()
                    except IntegrityError as exc2:
                        sp2.rollback()
                        result.violations.append(Violation(
                            doc["text_id"], "insert", "IntegrityError",
                            str(getattr(exc2, "orig", exc2)).split("\n")[0],
                        ))
                    if len(result.violations) == before:
                        result.violations.append(Violation(
                            doc["text_id"], "insert", "IntegrityError",
                            "bulk insert failed but the per-verse pass found nothing -- the "
                            "two paths disagree, which is itself the finding",
                        ))
            # D11: link the parts once every text row exists.
            for child, parent in PART_OF.items():
                conn.execute(
                    sa.text("UPDATE text SET part_of = :p WHERE id = :c AND EXISTS"
                            " (SELECT 1 FROM text WHERE id = :p)"),
                    {"p": parent, "c": child},
                )
            if dry_run:
                outer.rollback()
            elif result.violations and not allow_partial:
                # A knowingly-incomplete import is what the Mongo seeder already does: it
                # drops the 70 duplicates and logs a warning nobody reads (G8). Refusing to
                # commit is the difference. --allow-partial exists so the choice is explicit.
                outer.rollback()
            else:
                outer.commit()
        except Exception:
            outer.rollback()
            raise
    return result


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dsn", default=None, help="owner DSN; defaults to $CORPUS_OWNER_DSN")
    scope = ap.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true", help="import every text in scope")
    scope.add_argument("--text", action="append", metavar="SLUG",
                       help="import one text; repeatable. The fast loop for curation work.")
    ap.add_argument("--allow-partial", action="store_true",
                    help="commit even though some rows violated a constraint. Off by default: "
                         "silently dropping the offenders is exactly what the Mongo seeder "
                         "does today (G8), and the whole point here is that it stops.")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the real INSERTs against the real constraints, then roll back. "
                         "Reports EVERY violation rather than aborting on the first.")
    args = ap.parse_args(argv)

    import os
    dsn = args.dsn or os.environ.get("CORPUS_OWNER_DSN")
    if not dsn:
        print("no DSN: pass --dsn or set CORPUS_OWNER_DSN", file=sys.stderr)
        return 2

    only = set(args.text) if args.text else None
    result = run(dsn, only=only, dry_run=args.dry_run,
                 allow_partial=args.allow_partial)

    mode = "DRY RUN (nothing written)" if args.dry_run else "IMPORT"
    print(f"{mode}: {result.texts} texts · {result.facets} facets · "
          f"{result.sections:,} sections · {result.verses:,} verses · "
          f"{result.annotations:,} annotations · {result.revisions:,} revisions")
    excluded = [t for t in result.skipped if t in EXCLUDED_TEXTS]
    if excluded:
        print(f"  excluded by decision ({len(excluded)}): {', '.join(sorted(set(excluded)))}")
        print(f"  reason: sanskrit_texts/exclusions.py · GOTCHAS G62")
    if result.violations:
        if not args.dry_run and not args.allow_partial:
            print("\n  NOTHING WAS COMMITTED — the import rolled back. Fix the data, or pass "
                  "--allow-partial to accept the loss deliberately.")
        print(f"\n{len(result.violations)} violation(s) — ALL of them, not just the first:\n")
        for v in result.violations:
            print(f"  {v}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
