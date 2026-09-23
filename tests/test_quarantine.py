"""Dot-prefixed directories are not corpus, and every ingestion walker must agree.

`.quarantine/` (2026-09-23) holds texts that reached the tree and are not fit to serve --
`deva_keralam` and `dharmasindhu`, both from REFUSED acquisition rows. Keeping rather than
deleting them means the bytes are still on disk, one `rglob` away from the store. The ONLY
thing standing between them and a clean provenance record in the database is that every
walker skips dot-prefixed path components.

That is a safety claim about code, so it ships with a test that constructs the input which
would break it -- `rule:safety-flag-needs-a-test`. Not "the constant is present": a text
placed inside a dot-prefixed directory must be UNREACHABLE from both ingestion walkers.

The fixture is synthetic on purpose. `.quarantine/` is gitignored, so a test that asserted
against its real contents would pass vacuously on a fresh clone -- absence reading as a pass
is `rule:discernment-checks` §2, and this file exists to catch exactly that shape of error.
The real directory is checked too, but only as a bonus and only when it is there.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from sanskrit_texts.importer import corpus_files
from sanskrit_texts.reader import load_corpus_from_json

# Both ingestion walkers, by the name they are called elsewhere. translation_audit.py and
# translation_backlog.py apply the same rule but only produce reports -- they cannot write
# to the store, so they are out of scope here.
WALKERS = ("reader.load_corpus_from_json", "importer.corpus_files")


def _text(text_id: str) -> dict:
    """The minimum shape both walkers recognise as a corpus text."""
    return {
        "text_id": text_id,
        "title_sa": "परीक्षा",
        "title_en": "Fixture",
        "category": "fixture",
        "chapters": [
            {
                "number": 1,
                "title": "अध्यायः",
                "shlokas": [
                    {"number": 1, "text": "क ख ग", "english": "", "hindi": "",
                     "status": "untranslated"}
                ],
            }
        ],
    }


def _write(root: pathlib.Path, rel: str, text_id: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(_text(text_id), ensure_ascii=False), encoding="utf-8")


def _ids(root: pathlib.Path) -> tuple[set[str], set[str]]:
    """What each walker can see under `root`, as (reader, importer)."""
    from_reader = set(load_corpus_from_json(root))
    from_importer = set()
    for path in corpus_files(root):
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(doc, dict) and "text_id" in doc:
            from_importer.add(doc["text_id"])
    return from_reader, from_importer


@pytest.fixture
def tree(tmp_path: pathlib.Path) -> pathlib.Path:
    """One visible text, and the same text hidden four ways."""
    _write(tmp_path, "Hora/Visible/Visible.json", "visible_text")
    _write(tmp_path, ".quarantine/DevaKeralam/DevaKeralam.json", "quarantined_top")
    _write(tmp_path, ".anything/Deep/Deep.json", "quarantined_other_name")
    _write(tmp_path, "Hora/.held-back/Nested/Nested.json", "quarantined_nested")
    _write(tmp_path, "Hora/Nadi/.DevaKeralam.json", "quarantined_dotfile")
    return tmp_path


def test_the_check_can_fail(tree: pathlib.Path) -> None:
    """The control. If the visible text is not found, every assertion below is vacuous.

    This is the input that makes the test meaningful: a walker that returned the empty set
    would satisfy every `not in` below while being completely broken.
    """
    from_reader, from_importer = _ids(tree)
    assert "visible_text" in from_reader, "reader found nothing -- the test proves nothing"
    assert "visible_text" in from_importer, "importer found nothing -- the test proves nothing"


@pytest.mark.parametrize(
    "hidden",
    [
        "quarantined_top",  # .quarantine/ itself
        "quarantined_other_name",  # the rule is the SHAPE, not the name `.quarantine`
        "quarantined_nested",  # dot-prefixed component below the top level
        "quarantined_dotfile",  # a dot-prefixed FILE, not only a directory
    ],
)
def test_dot_prefixed_is_unreachable(tree: pathlib.Path, hidden: str) -> None:
    from_reader, from_importer = _ids(tree)
    assert hidden not in from_reader, f"reader.load_corpus_from_json reached {hidden}"
    assert hidden not in from_importer, f"importer.corpus_files reached {hidden}"


def test_real_quarantine_is_unreachable() -> None:
    """The live directory, when it is present. Skipped on a clone that has none.

    An attributable skip, not a silent pass -- the mechanism is already proven above
    against a fixture that is always there.
    """
    repo = pathlib.Path(__file__).resolve().parent.parent
    quarantine = repo / ".quarantine"
    if not quarantine.is_dir():
        pytest.skip("no .quarantine/ in this working tree (it is gitignored)")

    present = {
        json.loads(p.read_text(encoding="utf-8"))["text_id"]
        for p in quarantine.rglob("*.json")
        if "text_id" in json.loads(p.read_text(encoding="utf-8"))
    }
    assert present, ".quarantine/ holds no text_id-bearing JSON -- nothing was tested"

    from_reader, from_importer = _ids(repo)
    leaked = (present & from_reader) | (present & from_importer)
    assert not leaked, f"quarantined text(s) reachable from the corpus walkers: {sorted(leaked)}"
