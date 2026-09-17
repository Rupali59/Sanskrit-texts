"""§4's cutover gate: `export --mode fidelity` must reproduce the committed corpus.

IF THIS FAILS, THE IMPORT LOST SOMETHING. That is the whole claim, and it is the one that
decides whether the database can become authoritative.

TWO THINGS THIS DELIBERATELY DOES NOT DO.

**It does not shell out to `git diff --no-index --stat . /tmp/rt`.** That command was the
plan's original gate and it cannot go green: `.` is the repo root, so `scripts/`, `docs/`,
`migrations/`, `tests/` and `.venv-corpus/` all appear as deletions, and `--stat` collapses
the real corpus differences into line counts among that noise. A gate that is red for the
wrong reason gets loosened, and then it is a gate that cannot fail.

**It does not compare bytes.** Byte equality would additionally assert a Unicode normalisation
decision that has not been made -- 4 texts are not NFC, and whether import normalises them or
preserves them is open (OQ2). This compares PARSED structures, so it is sound either way; the
byte-level assertion belongs here too, scoped to that decision, once it lands.

TWO DECLARED NORMALISATIONS, because a round-trip with undeclared fudge is not a round-trip:

1. **An empty value and an absent key are the same fact.** The importer creates no annotation
   for `""` or `[]`, so the export omits the key. 1,307 verses carry an empty `english_draft`
   in the source.
2. **The 70 G8 duplicate labels are excluded.** Two verses sharing `(chapter, number)` cannot
   both exist under `uq_verse_label_in_section`; the importer REFUSES them and names all 70.
   The survivor is the first, while a source dict keyed by number keeps the last, so comparing
   them compares different verses. They are data to fix, tracked, and not a round-trip defect.
"""

from __future__ import annotations

import collections
import json
import pathlib

import pytest
import sqlalchemy as sa

from sanskrit_texts.export import build_doc
from sanskrit_texts.importer import import_text, load_corpus

# Chosen for SHAPE, not size -- between them these cover every hard case the corpus holds.
SHAPES = {
    "yajusha_jyotisham": "mixes int and str `number` in one text (4 texts do)",
    "mundaka_upanishad": "3-level tree, 2-component dotted labels",
    "prashna_upanishad": "dotted labels AND a populated `ref` on every verse",
    "garga_hora": "english_draft on every verse, none served",
    "bphs": "3,937 verses, tags with order and namespace, Devanagari-suffixed chapter labels",
}


def _norm(value):
    """Declared normalisation 1: empty and absent are the same fact."""
    return None if value in ("", [], {}) else value


def _index(chapter):
    return {(type(s["number"]).__name__, str(s["number"])): s for s in chapter["shlokas"]}


def _dupe_labels(chapter) -> set:
    counts = collections.Counter(
        (type(s["number"]).__name__, str(s["number"])) for s in chapter["shlokas"]
    )
    return {k for k, n in counts.items() if n > 1}


@pytest.fixture(scope="module")
def corpus_docs():
    docs = {d["text_id"]: d for _, d in load_corpus(set(SHAPES))}
    missing = set(SHAPES) - set(docs)
    if missing:
        pytest.skip(f"corpus JSON absent for {sorted(missing)} -- absent, not a pass")
    return docs


@pytest.mark.parametrize("text_id", sorted(SHAPES), ids=sorted(SHAPES))
def test_export_reproduces_the_committed_corpus(owner_engine, clean_corpus, corpus_docs,
                                                text_id: str):
    source = corpus_docs[text_id]
    with owner_engine.begin() as conn:
        result = type("R", (), {"texts": 0, "sections": 0, "verses": 0, "annotations": 0,
                                "revisions": 0, "facets": 0, "skipped": [], "violations": []})()
        import_text(conn, source, result, enumerate_all=True)
        exported = build_doc(conn, text_id, mode="fidelity")

    assert exported is not None, f"{text_id} imported but exported nothing"
    for key in ("text_id", "title_sa", "title_en", "category", "structure"):
        assert source.get(key) == exported.get(key), f"{text_id}: top-level {key!r} differs"

    src_ch = {str(c["number"]): c for c in source["chapters"]}
    exp_ch = {str(c["number"]): c for c in exported["chapters"]}
    assert set(src_ch) == set(exp_ch), f"{text_id}: chapter set differs"

    differences: list[str] = []
    for number, s_chapter in src_ch.items():
        e_chapter = exp_ch[number]
        for key in ("title", "title_en"):
            if s_chapter.get(key) != e_chapter.get(key):
                differences.append(f"chapter {number}: {key!r}")
        skip = _dupe_labels(s_chapter)          # declared normalisation 2
        s_v, e_v = _index(s_chapter), _index(e_chapter)
        # ORDER, not just membership. `_index` is a dict, so a check built only on it cannot see
        # verses coming back in the wrong sequence -- which is exactly how an exporter that
        # grouped by section passed this test while reordering 3 real texts (2026-09-17).
        s_order = [k for k in ((type(x["number"]).__name__, str(x["number"])) for x in s_chapter["shlokas"]) if k not in skip]
        e_order = [k for k in ((type(x["number"]).__name__, str(x["number"])) for x in e_chapter["shlokas"]) if k not in skip]
        if s_order != e_order:
            first = next((i for i, (a, b) in enumerate(zip(s_order, e_order, strict=False)) if a != b), None)
            differences.append(f"chapter {number}: verse ORDER differs at index {first}: "
                               f"{s_order[first:first + 3] if first is not None else s_order[-3:]} != "
                               f"{e_order[first:first + 3] if first is not None else e_order[-3:]}")
        for missing in sorted(set(s_v) - set(e_v) - skip):
            differences.append(f"chapter {number}: verse {missing} absent from the export")
        for key in sorted((set(s_v) & set(e_v)) - skip):
            for field in ("text", "english", "hindi", "english_draft", "hindi_draft",
                          "status", "ref", "meter", "tags", "tags_draft"):
                if _norm(s_v[key].get(field)) != _norm(e_v[key].get(field)):
                    differences.append(
                        f"chapter {number} verse {key} field {field!r}: "
                        f"{_norm(s_v[key].get(field))!r} != {_norm(e_v[key].get(field))!r}"
                    )
    assert not differences, (
        f"{text_id} ({SHAPES[text_id]}) did not round-trip:\n  "
        + "\n  ".join(differences[:20])
        + (f"\n  ... and {len(differences) - 20} more" if len(differences) > 20 else "")
    )


def test_the_roundtrip_check_can_actually_fail(owner_engine, clean_corpus, corpus_docs):
    """rule:discernment-checks §1 -- ship the input that makes it fail.

    Imports a text with ONE verse's Devanagari altered, and asserts the comparison notices.
    Without this, a comparison whose field list was empty, or whose index keys never matched,
    would report a perfect round-trip forever.
    """
    # Deep-copy only the JSON-native keys: load_corpus attaches `_path` (a PosixPath) and
    # `_sha`, and json.dumps chokes on the first.
    original = corpus_docs["yajusha_jyotisham"]
    source = json.loads(json.dumps(
        {k: v for k, v in original.items() if not k.startswith("_")}
    ))
    source["_path"] = original["_path"]
    source["_sha"] = original["_sha"]
    victim = source["chapters"][0]["shlokas"][0]
    victim["text"] = victim["text"] + "ॐ"      # append OM; one character
    with owner_engine.begin() as conn:
        result = type("R", (), {"texts": 0, "sections": 0, "verses": 0, "annotations": 0,
                                "revisions": 0, "facets": 0, "skipped": [], "violations": []})()
        import_text(conn, source, result, enumerate_all=True)
        exported = build_doc(conn, "yajusha_jyotisham", mode="fidelity")

    pristine = corpus_docs["yajusha_jyotisham"]
    s_v = _index(pristine["chapters"][0])
    e_v = _index(exported["chapters"][0])
    key = next(iter(s_v))
    assert _norm(s_v[key].get("text")) != _norm(e_v[key].get("text")), (
        "a one-character change to a verse did not show up in the comparison -- the "
        "round-trip check cannot detect loss"
    )


def test_citable_mode_carries_no_unapproved_value(owner_engine, clean_corpus, corpus_docs):
    """`--mode citable` is the released dataset, and nothing in the corpus is approved yet.

    Everything imports `draft` (UC1), so a citable export today must contain ZERO annotations.
    That is not a bug -- it is the gate working before any human has reviewed anything.
    """
    source = corpus_docs["garga_hora"]
    with owner_engine.begin() as conn:
        result = type("R", (), {"texts": 0, "sections": 0, "verses": 0, "annotations": 0,
                                "revisions": 0, "facets": 0, "skipped": [], "violations": []})()
        import_text(conn, source, result, enumerate_all=True)
        fidelity = build_doc(conn, "garga_hora", mode="fidelity")
        citable = build_doc(conn, "garga_hora", mode="citable")

    def annotation_keys(doc):
        return [f for c in doc["chapters"] for s in c["shlokas"]
                for f in ("english", "hindi", "english_draft", "hindi_draft", "tags",
                          "tags_draft")
                if s.get(f)]

    assert annotation_keys(fidelity), "fidelity mode carried nothing -- the negative control"
    assert not annotation_keys(citable), (
        "citable mode carried an annotation, but nothing in the corpus is `approved`"
    )


def test_export_keeps_array_order_when_depths_interleave(owner_engine, clean_corpus):
    """A subdivided unit BETWEEN two plain ones: `1.66`, `1.66.1`, `1.67`. None of SHAPES has
    this, and the exporter got it wrong until 2026-09-17 (it emitted `1.66.1` after `1.67`)."""
    doc = {
        "text_id": "interleave_fixture", "title_sa": "x", "title_en": "x", "category": "parashari",
        "structure": {"levels": ["chapter", "level2", "level3", "verse"]},
        "chapters": [{"number": 1, "shlokas": [
            {"number": "1.66", "text": "क", "status": "untranslated"},
            {"number": "1.66.1", "text": "ख", "status": "untranslated"},
            {"number": "1.67", "text": "ग", "status": "untranslated"},
            {"number": "2.1", "text": "घ", "status": "untranslated"},
            {"number": "1.68", "text": "ङ", "status": "untranslated"},
        ]}],
        "_sha": "0" * 64, "_path": pathlib.Path(__file__).resolve().parent.parent / "Hora" / "x" / "x.json",
    }
    with owner_engine.begin() as conn:
        result = type("R", (), {"texts": 0, "sections": 0, "verses": 0, "annotations": 0,
                                "revisions": 0, "facets": 0, "skipped": [], "violations": []})()
        import_text(conn, doc, result, enumerate_all=True)
        assert not result.violations, result.violations
        exported = build_doc(conn, "interleave_fixture", mode="fidelity")
    got = [str(s["number"]) for s in exported["chapters"][0]["shlokas"]]
    assert got == ["1.66", "1.66.1", "1.67", "2.1", "1.68"], got
