"""A corpus file that cannot be read must be REPORTED, never skipped quietly.

Until 2026-09-23 `importer.load_corpus` swallowed `OSError` and `json.JSONDecodeError`
with a bare `continue`. A truncated or mid-write JSON vanished from the import with no
message, no `Violation`, and exit 0 -- and in scoped mode (`--text x` on a corrupt `x`)
the run printed `0 texts · 0 verses` and committed, so a corrupted file looked exactly
like a typo'd slug.

That is G8's silent-loss shape moved from the row boundary to the file boundary, and
`rule:discernment-checks` §2 is the rule it breaks: absence must be attributable.

The tests below construct the input that the old code lost. Per
`rule:safety-flag-needs-a-test` they assert the EFFECT (a Violation recorded, a line on
stderr) rather than that a try/except is present, and `test_the_control` fails if the
loader stops finding the good file -- without it every `in` assertion here could pass
against a loader that returned everything unconditionally.

Note for whoever edits these: `corpus_files` takes `root: pathlib.Path = REPO` as a
DEFAULT ARGUMENT, bound at definition time. Reassigning `importer.REPO` does NOT redirect
it -- an audit did exactly that, silently walked the real 66-text corpus, and reported a
result it had not produced. Patch the FUNCTION, as `_loader` does.
"""

from __future__ import annotations

import json
import pathlib

import pytest

import sanskrit_texts.importer as importer

GOOD = {
    "text_id": "zz_good",
    "title_sa": "परीक्षा",
    "title_en": "Fixture",
    "category": "fixture",
    "chapters": [{"number": 1, "title": "अ", "shlokas": [
        {"number": 1, "text": "क ख ग", "english": "", "hindi": "", "status": "untranslated"}
    ]}],
}


@pytest.fixture
def tree(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> pathlib.Path:
    """One good text, one truncated, one that lost its body, one that is not corpus at all."""
    (tmp_path / "Good").mkdir()
    (tmp_path / "Good" / "g.json").write_text(json.dumps(GOOD), encoding="utf-8")

    (tmp_path / "Truncated").mkdir()
    (tmp_path / "Truncated" / "t.json").write_text(
        '{"text_id": "zz_truncated", "chapters": [{"number": 1, "shlokas": [{"num',
        encoding="utf-8")

    (tmp_path / "Bodyless").mkdir()
    (tmp_path / "Bodyless" / "b.json").write_text(
        json.dumps({"text_id": "zz_bodyless", "title_en": "lost its chapters"}),
        encoding="utf-8")

    # Not a corpus file at all. Silence for THIS one is correct: the tree may hold
    # unrelated JSON and flagging it would cry wolf.
    (tmp_path / "NotCorpus").mkdir()
    (tmp_path / "NotCorpus" / "config.json").write_text(
        json.dumps({"some": "unrelated config"}), encoding="utf-8")

    monkeypatch.setattr(importer, "corpus_files",
                        lambda root=tmp_path: sorted(tmp_path.rglob("*.json")))
    return tmp_path


def test_the_control(tree: pathlib.Path) -> None:
    """The loader still finds the good text. Without this, every assertion below is vacuous."""
    problems: list[importer.Violation] = []
    found = {d["text_id"] for _, d in importer.load_corpus(problems=problems)}
    assert "zz_good" in found, "loader found nothing — the rest of this file proves nothing"


@pytest.mark.parametrize("text_id,kind", [
    ("zz_truncated", "JSONDecodeError"),
    ("zz_bodyless", "missing-chapters"),
])
def test_an_unreadable_file_is_recorded(tree: pathlib.Path, text_id: str, kind: str) -> None:
    problems: list[importer.Violation] = []
    found = {d["text_id"] for _, d in importer.load_corpus(problems=problems)}

    assert text_id not in found, f"{text_id} parsed — fixture is wrong, not the loader"
    kinds = {v.kind for v in problems}
    assert kind in kinds, (
        f"{text_id} was dropped with no Violation recorded. Got {kinds or 'nothing'} — this is "
        f"the silent-loss defect this file exists to pin."
    )


def test_a_non_corpus_json_is_NOT_flagged(tree: pathlib.Path) -> None:
    """The other half. A guard that fires on everything is as useless as one that never does."""
    problems: list[importer.Violation] = []
    importer.load_corpus(problems=problems)
    assert not [v for v in problems if "config.json" in v.where], (
        "unrelated JSON was reported as a corpus failure — that is crying wolf, and it "
        "trains the reader to ignore the real ones"
    )


def test_stderr_carries_it_even_with_no_problems_list(
    tree: pathlib.Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """A caller that passes no list must still be unable to lose a file silently."""
    importer.load_corpus()
    err = capsys.readouterr().err
    assert "UNREADABLE" in err and "zz_truncated" in err.replace("t.json", "zz_truncated"), (
        f"nothing on stderr for an unreadable file; got {err!r}"
    )


def test_scoped_mode_does_not_look_like_success(tree: pathlib.Path) -> None:
    """The worst shape of the original bug, pinned.

    `load_corpus(only={"zz_truncated"})` returned `[]` with an empty violations list, so
    `run()` committed and printed `0 texts · 0 verses`, exit 0 — a corrupt file rendered
    identically to a slug that never existed.
    """
    corrupt: list[importer.Violation] = []
    importer.load_corpus(only={"zz_truncated"}, problems=corrupt)

    typo: list[importer.Violation] = []
    importer.load_corpus(only={"zz_never_existed"}, problems=typo)

    assert corrupt, "a corrupt named text reported nothing"
    assert not typo, "a slug that does not exist should report nothing — it is not a failure"
    assert corrupt != typo, "corrupt file and typo'd slug are still indistinguishable"
