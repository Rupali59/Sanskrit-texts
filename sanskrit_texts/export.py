"""Write the corpus back out as JSON. Two modes, and they are not the same artifact.

WHY TWO MODES. An earlier draft of this design required ONE export to satisfy both "the
sentinel appears in zero bytes" and "semantically equal to the committed corpus" -- and the
committed corpus contains thousands of draft values, so both could not hold. They are
different artifacts for different jobs:

  --mode fidelity   everything, drafts included. THE CUTOVER GATE: if this does not reproduce
                    the committed corpus, the import lost something. Never served, never
                    published.
  --mode citable    approved annotations only. The dataset release. The no-draft-bytes
                    assertion scopes to THIS.

ONE `--mode`, NOT TWO BOOLEANS. `--fidelity` and `--citable` as separate flags make
"both" and "neither" representable, and neither is a thing. There is no default: an export
that silently picks the never-servable mode is a footgun pointing the other way.

THE SERIALIZATION CONTRACT IS PART OF THE DELIVERABLE, not an implementation detail. After
cutover this exporter WRITES the tracked JSON, so every future `git diff` in the repo depends
on these four choices being stable:

    json.dumps(doc, ensure_ascii=False, indent=2) + "\\n"

`ensure_ascii=False` because the corpus is Devanagari and escaping it would quadruple the
file and make every diff unreadable; `indent=2` to match what is committed; insertion key
order, never `sort_keys`, because the source order is `text_id` first and that is worth
keeping; one trailing newline.

WHAT THIS DOES NOT DECIDE. Unicode normalisation is still open (4 texts are not NFC). This
exporter reproduces the bytes it was given and normalises nothing, so the round-trip is sound
either way -- but a byte-level assertion cannot be made until that decision lands.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
from typing import Any

import sqlalchemy as sa

from sanskrit_texts.exclusions import EXCLUDED_TEXTS

INDENT = 2
ENSURE_ASCII = False
TRAILING_NEWLINE = "\n"

# `citable` serves only what a named human approved. `fidelity` serves everything, because its
# job is to prove nothing was lost.
CITABLE_STATES = ("approved",)


def serialize(doc: dict[str, Any]) -> str:
    """The contract, in one place, so both the exporter and its test cite the same function."""
    return json.dumps(doc, ensure_ascii=ENSURE_ASCII, indent=INDENT) + TRAILING_NEWLINE


def _verse_number(label: str, is_str: bool) -> Any:
    """Restore the JSON type. 32 labels are digit-strings that were typed `str`."""
    if is_str:
        return label
    try:
        return int(label)
    except ValueError:
        return label


def _chapter_number(label: str) -> Any:
    try:
        return int(label)
    except ValueError:
        return label


def build_doc(conn: sa.Connection, text_id: str, *, mode: str) -> dict[str, Any] | None:
    """Reconstruct one text's JSON from the store."""
    row = conn.execute(
        sa.text("SELECT id, title_sa, title_en, category, structure, source_sha"
                " FROM text WHERE id = :t"),
        {"t": text_id},
    ).mappings().first()
    if row is None:
        return None
    # A text with no source_sha came from no file -- the synthetic parent work created for
    # `part_of`. Exporting it would invent a corpus file that never existed.
    if row["source_sha"] is None:
        return None

    doc: dict[str, Any] = {"text_id": row["id"]}
    if row["title_sa"] is not None:
        doc["title_sa"] = row["title_sa"]
    if row["title_en"] is not None:
        doc["title_en"] = row["title_en"]
    if row["category"] is not None:
        doc["category"] = row["category"]
    if row["structure"] is not None:
        doc["structure"] = row["structure"]

    sections = conn.execute(
        sa.text("SELECT id, parent_id, depth, label, title, title_en, position"
                " FROM section WHERE text_id = :t ORDER BY depth, position, id"),
        {"t": text_id},
    ).mappings().all()
    by_id = {s["id"]: s for s in sections}

    def label_path(section_id: int) -> list[str]:
        """Every label from below the chapter down to this section."""
        out: list[str] = []
        cur = by_id.get(section_id)
        while cur is not None and cur["parent_id"] is not None:
            out.append(cur["label"])
            cur = by_id.get(cur["parent_id"])
        return list(reversed(out))

    def root_of(section_id: int) -> int:
        cur = by_id[section_id]
        while cur["parent_id"] is not None:
            cur = by_id[cur["parent_id"]]
        return cur["id"]

    verses = conn.execute(
        sa.text("SELECT id, section_id, number_label, number_is_str, position, devanagari,"
                " ref, meter, status FROM verse WHERE section_id IN"
                " (SELECT id FROM section WHERE text_id = :t) ORDER BY section_id, position"),
        {"t": text_id},
    ).mappings().all()

    ann_by_verse: dict[int, list[Any]] = {}
    if verses:
        state_clause = ""
        params: dict[str, Any] = {"t": text_id}
        if mode == "citable":
            state_clause = " AND a.state = ANY(:states)"
            params["states"] = list(CITABLE_STATES)
        rows = conn.execute(
            sa.text(
                "SELECT a.verse_id, a.kind, a.lang, a.value, a.position, a.source_field"
                " FROM annotation a WHERE a.verse_id IN (SELECT v.id FROM verse v JOIN section s"
                " ON s.id = v.section_id WHERE s.text_id = :t)" + state_clause +
                " ORDER BY a.verse_id, a.position NULLS FIRST, a.id"
            ),
            params,
        ).mappings().all()
        for r in rows:
            ann_by_verse.setdefault(r["verse_id"], []).append(r)

    chapters: dict[int, dict[str, Any]] = {}
    for s in sections:
        if s["parent_id"] is None:
            ch: dict[str, Any] = {"number": _chapter_number(s["label"])}
            if s["title"] is not None:
                ch["title"] = s["title"]
            if s["title_en"] is not None:
                ch["title_en"] = s["title_en"]
            ch["shlokas"] = []
            chapters[s["id"]] = ch

    for v in verses:
        path = label_path(v["section_id"]) + [v["number_label"]]
        number = _verse_number(".".join(path), v["number_is_str"])
        sh: dict[str, Any] = {"number": number, "text": v["devanagari"]}
        anns = ann_by_verse.get(v["id"], [])
        for field in ("english", "hindi", "english_draft", "hindi_draft"):
            hit = next((a for a in anns if a["source_field"] == field), None)
            if hit is not None:
                sh[field] = hit["value"]
        for field in ("tags", "tags_draft"):
            vals = [a["value"] for a in anns if a["source_field"] == field]
            if vals:
                sh[field] = vals
        if v["status"] is not None:
            sh["status"] = v["status"]
        if v["ref"] is not None:
            sh["ref"] = v["ref"]
        if v["meter"] is not None:
            sh["meter"] = v["meter"]
        chapters[root_of(v["section_id"])]["shlokas"].append(sh)

    doc["chapters"] = [chapters[s["id"]] for s in sections if s["parent_id"] is None]
    return doc


def run(dsn: str, *, out: pathlib.Path, mode: str, only: set[str] | None) -> dict[str, int]:
    engine = sa.create_engine(dsn, future=True)
    out.mkdir(parents=True, exist_ok=True)
    stats = {"texts": 0, "verses": 0}
    with engine.connect() as conn:
        ids = conn.execute(sa.text("SELECT id FROM text ORDER BY id")).scalars().all()
        for tid in ids:
            if tid in EXCLUDED_TEXTS or (only is not None and tid not in only):
                continue
            doc = build_doc(conn, tid, mode=mode)
            if doc is None:
                continue
            (out / f"{tid}.json").write_text(serialize(doc), encoding="utf-8")
            stats["texts"] += 1
            stats["verses"] += sum(len(c["shlokas"]) for c in doc["chapters"])
    return stats


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dsn", default=None, help="defaults to $CORPUS_OWNER_DSN")
    ap.add_argument("--mode", choices=("fidelity", "citable"), required=True,
                    help="fidelity = everything incl. drafts, for the cutover gate. "
                         "citable = approved only, for the dataset release. No default.")
    ap.add_argument("--out", required=True, type=pathlib.Path)
    scope = ap.add_mutually_exclusive_group(required=True)
    scope.add_argument("--all", action="store_true")
    scope.add_argument("--text", action="append", metavar="SLUG")
    args = ap.parse_args(argv)

    dsn = args.dsn or os.environ.get("CORPUS_OWNER_DSN")
    if not dsn:
        print("no DSN: pass --dsn or set CORPUS_OWNER_DSN", file=sys.stderr)
        return 2
    stats = run(dsn, out=args.out, mode=args.mode,
                only=set(args.text) if args.text else None)
    print(f"EXPORT --mode {args.mode}: {stats['texts']} texts · {stats['verses']:,} verses "
          f"-> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
