"""`sanskrit_texts.reader` -- the first real consumer of the store (plan §5).

THREE CLAIMS THE MODULE DOCSTRING MAKES, EACH PROVEN HERE, NOT JUST ASSERTED IN PROSE.

1. `load_corpus_from_db` connects with `CORPUS_API_DSN` by default and NEVER falls back to
   `CORPUS_OWNER_DSN`, even when it is set. The whole publication gate (docs/DATABASE.md)
   rests on no consumer holding the owner DSN; a reader that silently preferred owner would be
   the first place that promise broke, so this is proven by giving it a BROKEN api DSN and a
   WORKING owner DSN and asserting it fails rather than quietly succeeding on the wrong one.
2. An empty store is a `RuntimeError` naming the reason, never a bare `{}`. A reader that
   cannot report failure returns absence, which is worse than a wrong answer because absence
   is actionable and gets acted on (`rule:discernment-checks` §6).
3. The json and db sources agree on the fields both can see in full -- text count and shloka
   count for a text imported into both. They are NOT asserted to agree field-for-field; see
   `reader.py`'s module docstring for exactly which fields the db source cannot supply and why.

FOUR MORE CLAIMS, FOR THE VERSE-LEVEL API (`load_text_from_json`), THE §5 SCRIPT MIGRATION.

4. It returns the verses a known small text actually holds. `yajusha_jyotisham` (45 verses,
   1 chapter) is used rather than `bphs` (thousands, and mid-flux — see STATE.md) precisely
   because its shape is small enough to assert exactly, not approximately.
5. It never imports `sqlalchemy`, even indirectly, on the json path -- proven in a SUBPROCESS
   with a fresh interpreter, because a `sys.modules` check in-process would only prove sqlalchemy
   was not ALREADY imported by something else in this test session, not that this call is what
   keeps it out (`tests/test_key_census.py` and others in this same session import it freely).
6. Pointed at a directory with no corpus at all, it raises a NAMED failure, never a bare `{}`
   or `(None, None)` -- the same "absence must be attributable" claim `load_corpus_from_db`
   already makes for the db source (claim 2 above), now for the json-side verse lookup.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys

import pytest
import sqlalchemy as sa

from sanskrit_texts import reader
from sanskrit_texts.importer import import_text
from sanskrit_texts.importer import load_corpus as load_importer_corpus

REPO = pathlib.Path(__file__).resolve().parent.parent

# Mirrors conftest.py's API_DSN default deliberately, rather than importing it -- conftest is
# not a public module of this package, and duplicating one DSN string costs less than depending
# on pytest's conftest-as-importable-module behaviour holding across configurations. The owner
# DSN is never needed directly here: `owner_engine` (from conftest) supplies it as a fixture.
API_DSN = os.environ.get(
    "CORPUS_API_DSN",
    "postgresql+psycopg://corpus_api:corpus_api_local@127.0.0.1:5433/sanskrit_texts_test",
)

# Small and clean: no duplicate-label violations, so it imports without --allow-partial.
# Also the text `make hello` uses for the same reason -- a real, fast, unsurprising fixture.
SAMPLE_TEXT = "yajusha_jyotisham"


def _import_one(owner_engine: sa.engine.Engine, text_id: str) -> None:
    [(_, doc)] = load_importer_corpus(only={text_id})
    with owner_engine.begin() as conn:
        result = type(
            "R",
            (),
            {
                "texts": 0,
                "sections": 0,
                "verses": 0,
                "annotations": 0,
                "revisions": 0,
                "facets": 0,
                "skipped": [],
                "violations": [],
            },
        )()
        import_text(conn, doc, result, enumerate_all=True)
    assert not result.violations, (
        f"fixture import of {text_id!r} was not clean: {result.violations}"
    )


# --------------------------------------------------------------------------------------------
# 1. The DSN default -- no database needed. `create_engine` is intercepted before any socket
#    is opened, so this proves WHICH DSN was chosen without depending on either being live.
# --------------------------------------------------------------------------------------------


def test_db_source_defaults_to_api_dsn_never_owner(monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[str] = []

    def fake_create_engine(dsn: str, **kwargs):
        seen.append(dsn)
        raise RuntimeError("stop before any real connection is attempted")

    monkeypatch.setattr(sa, "create_engine", fake_create_engine)
    monkeypatch.setenv("CORPUS_API_DSN", "postgresql+psycopg://api-was-used/db")
    # A DIFFERENT, obviously-owner-shaped DSN. If the reader ever preferred this, `seen` would
    # record it instead, and the assertion below would catch it.
    monkeypatch.setenv("CORPUS_OWNER_DSN", "postgresql+psycopg://owner-must-not-be-used/db")

    with pytest.raises(RuntimeError, match="stop before any real connection"):
        reader.load_corpus_from_db()

    assert seen == ["postgresql+psycopg://api-was-used/db"], (
        f"expected exactly one connection attempt, against CORPUS_API_DSN; got {seen}"
    )


def test_db_source_never_reads_owner_dsn_env_var_at_all(monkeypatch: pytest.MonkeyPatch) -> None:
    """Same claim, proven the other way: unset CORPUS_API_DSN entirely (only CORPUS_OWNER_DSN
    is set) and confirm the reader refuses rather than falling back to it."""
    monkeypatch.delenv("CORPUS_API_DSN", raising=False)
    monkeypatch.setenv("CORPUS_OWNER_DSN", "postgresql+psycopg://owner-must-not-be-used/db")

    with pytest.raises(RuntimeError, match="CORPUS_API_DSN"):
        reader.load_corpus_from_db()


def test_load_corpus_dispatcher_rejects_unknown_source() -> None:
    with pytest.raises(ValueError, match="unknown source"):
        reader.load_corpus(source="mongo")


# --------------------------------------------------------------------------------------------
# 2. Absence must be attributable (`rule:discernment-checks` §2/§6): an empty store is a
#    failure a caller can see, not a summary that happens to be `{}`.
# --------------------------------------------------------------------------------------------


def test_empty_store_raises_rather_than_returning_bare_zero(owner_engine, clean_corpus) -> None:
    with pytest.raises(RuntimeError, match="0 rows"):
        reader.load_corpus_from_db(dsn=API_DSN)


# --------------------------------------------------------------------------------------------
# 3. The two sources agree on what both can see in full.
# --------------------------------------------------------------------------------------------


def test_json_and_db_sources_agree_on_a_shared_text(owner_engine, api_engine, clean_corpus) -> None:
    _import_one(owner_engine, SAMPLE_TEXT)

    json_summary = reader.load_corpus_from_json(REPO)
    db_summary = reader.load_corpus_from_db(dsn=API_DSN)

    assert SAMPLE_TEXT in json_summary, "fixture text must exist in the real corpus JSON"
    assert SAMPLE_TEXT in db_summary, "the import above must have landed it in the store"

    j, d = json_summary[SAMPLE_TEXT], db_summary[SAMPLE_TEXT]
    assert d["sh"] == j["sh"], (
        f"{SAMPLE_TEXT}: shloka count disagrees -- json {j['sh']}, db {d['sh']} "
        f"(no duplicate labels are expected in this fixture, so no gap is allowed)"
    )
    assert d["cat"] == j["cat"], "category is fully visible through published_text"

    # The fields the db source deliberately cannot supply (reader.py's module docstring) --
    # asserted None, not merely "whatever it happens to return", so a future change that
    # starts guessing one of them is caught here rather than discovered downstream.
    for field in reader.DB_UNAVAILABLE_FIELDS:
        assert d[field] is None, f"{field!r} should be unavailable through the API source"

    # `tr`/`pct` measure REVIEW state through the db source, not arrival state (module
    # docstring). Nothing has been approved (STATE.md 2026-09-16: 0 approved rows), so this
    # must read 0 even though the json source's own `tr` for this text is nonzero -- proving
    # the two are different facts, not that one of them is broken.
    assert d["tr"] == 0
    assert d["pct"] == 0


def test_db_source_return_shape_matches_json_source(owner_engine, api_engine, clean_corpus) -> None:
    """Same nine keys either way -- callers must not have to branch on which source they used."""
    _import_one(owner_engine, SAMPLE_TEXT)
    json_summary = reader.load_corpus_from_json(REPO)
    db_summary = reader.load_corpus_from_db(dsn=API_DSN)
    expected_keys = {"ch", "sh", "tr", "pct", "dir", "cat", "dupes", "titles", "authority"}
    assert set(json_summary[SAMPLE_TEXT]) == expected_keys
    assert set(db_summary[SAMPLE_TEXT]) == expected_keys


# --------------------------------------------------------------------------------------------
# 4. `load_text_from_json` -- the verse-level API `tag_features.py` and `spot_check.py` now
#    share (§5). No database needed for any of these; all three are pure-json claims.
# --------------------------------------------------------------------------------------------

# A small, single-chapter, non-fluctuating text -- unlike `bphs`, which STATE.md records as
# mid-migration -- so the exact verse count in the assertion below cannot rot out from under it.
SMALL_TEXT = "yajusha_jyotisham"
SMALL_TEXT_VERSES = 45


def test_load_text_from_json_returns_the_verses_a_known_small_text_holds() -> None:
    doc, rel = reader.load_text_from_json(SMALL_TEXT, root=REPO)

    assert doc["text_id"] == SMALL_TEXT
    verses = [sh for ch in doc["chapters"] for sh in ch["shlokas"]]
    assert len(verses) == SMALL_TEXT_VERSES, (
        f"{SMALL_TEXT} is expected to hold exactly {SMALL_TEXT_VERSES} verses; got "
        f"{len(verses)}. If this text was re-digitised, update SMALL_TEXT_VERSES to match --  "
        f"this assertion exists to catch the reader silently returning the wrong document, not "
        f"to pin the corpus's editorial state."
    )
    # `rel` is a real, resolvable path back to the same file -- `tag_features.py` needs this to
    # write the file back after tagging (its write path is untouched by this migration).
    assert (REPO / rel).is_file()
    on_disk = json.loads((REPO / rel).read_text(encoding="utf-8"))
    assert on_disk["text_id"] == SMALL_TEXT


def test_load_text_from_json_unknown_text_id_raises_named_error() -> None:
    """A text_id that exists nowhere in the real corpus -- distinct from claim 6 below, which
    points at a directory holding no corpus at all."""
    with pytest.raises(reader.TextNotFoundError, match="no-such-text-id-in-this-corpus"):
        reader.load_text_from_json("no-such-text-id-in-this-corpus", root=REPO)


def test_load_text_from_json_empty_directory_reports_clearly_not_a_bare_empty(
    tmp_path: pathlib.Path,
) -> None:
    """Claim 6: pointed at a directory with no corpus JSON at all, this must not return an
    empty document, `None`, or any other value quietly standing in for "nothing here" --
    `rule:discernment-checks` §2/§6. It must raise something a caller can see and name."""
    with pytest.raises(reader.TextNotFoundError, match=str(tmp_path)):
        reader.load_text_from_json("bphs", root=tmp_path)


def test_load_text_from_json_does_not_import_sqlalchemy() -> None:
    """Proven in a FRESH subprocess, not an in-process `sys.modules` check -- this test session
    already imports sqlalchemy for the db-facing tests above, so checking `sys.modules` here
    would prove nothing about what `load_text_from_json` itself pulls in. A clean interpreter
    that only imports `sanskrit_texts.reader` and calls the json-path function is the only way
    to prove the claim the module docstring makes: the JSON path stays dependency-free, so
    `check_inventory.py` -- and now `tag_features.py`/`spot_check.py` -- keep working under bare
    system `python3` with nothing installed."""
    script = (
        "import pathlib, sys\n"
        f"sys.path.insert(0, {str(REPO)!r})\n"
        "from sanskrit_texts import reader\n"
        f"reader.load_text_from_json({SMALL_TEXT!r}, root=pathlib.Path({str(REPO)!r}))\n"
        "assert 'sqlalchemy' not in sys.modules, sorted(m for m in sys.modules if 'sqlalchemy' in m)\n"
        "print('OK')\n"
    )
    result = subprocess.run(
        [sys.executable, "-c", script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"subprocess failed (sqlalchemy import or lookup broke):\n"
        f"stdout={result.stdout!r}\nstderr={result.stderr!r}"
    )
    assert result.stdout.strip() == "OK"


@pytest.mark.parametrize(
    ("verses", "expected"),
    [
        (["translated", "translated"], "translated"),
        (["translated", "drafted"], "partial"),
        (["partial", "drafted"], "partial"),
        (["untranslated", "drafted"], "drafted"),
        (["untranslated", None], "untranslated"),
        ([], "untranslated"),  # all() over nothing is True; an empty text translated nothing
    ],
)
def test_derive_text_status_rule(verses: list[str | None], expected: str) -> None:
    assert reader.derive_text_status(verses) == expected


def test_every_text_level_status_equals_its_derivation() -> None:
    """A cached summary is only safe if something re-derives it. The 28 text-level `status`
    values were stamped `translated` on 2026-09-16 and were false on 17 texts by that evening,
    with every test green. This is the check that was missing: change a verse, forget the text,
    and this names the text."""
    from sanskrit_texts.exclusions import EXCLUDED_TEXTS

    carrying, wrong = 0, []
    for path in sorted(REPO.rglob("*.json")):
        rel = path.relative_to(REPO)
        if rel.parts[0] == "docs" or any(p.startswith(".") for p in rel.parts):
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if "chapters" not in doc or "status" not in doc or doc.get("text_id") in EXCLUDED_TEXTS:
            continue
        carrying += 1
        derived = reader.derive_text_status(
            s.get("status") for c in doc["chapters"] for s in c["shlokas"]
        )
        if doc["status"] != derived:
            wrong.append(f"{doc['text_id']}: file says {doc['status']!r}, verses say {derived!r}")
    # Absence must be attributable: zero files carrying the key is a finding, not a pass.
    assert carrying, "no corpus file carries a text-level status -- corpus missing, or key gone"
    assert not wrong, "\n".join(wrong)
