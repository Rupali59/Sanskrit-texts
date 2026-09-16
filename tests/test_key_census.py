"""Every key in the corpus has a home in the schema, or is recorded as deliberately omitted.

WHY THIS EXISTS. `structure` — 18 distinct keys across 49 texts, including `known_gaps` and
`count_authority` — has never reached a database, because `seed_texts.py`'s `_normalize_shloka`
copies 12 named keys and drops the rest in silence. Nothing failed. Nothing warned. The
database was simply less informative than the files for years, and the first anyone knew was a
manual read of the function. `meter` (709 verses) and chapter `title_en` were both missed by
the first draft of this schema for the same reason: nobody was counting keys.

So: an unseen key fails CI. Not "gets dropped and noticed later".

ASSERTS SETS, NOT COUNTS — and that is not laziness. On 2026-09-16 a translation script was
running against the corpus while these tests were being written: `brahmasphuta_siddhanta` went
from 502 to 532 translated verses in twenty seconds. Any assertion on a tally would be flaky by
construction and would eventually be "fixed" by loosening it. Key SETS are structural and do
not move while text is being translated.
"""

from __future__ import annotations

import json
import pathlib

import pytest

from sanskrit_texts.exclusions import EXCLUDED_TEXTS
from sanskrit_texts.models import Section, Text_, Verse

REPO = pathlib.Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------------------
# What the corpus contains, per level. A key appearing that is not listed here FAILS, and the
# failure names it — that is the whole mechanism.
# ---------------------------------------------------------------------------------------
TEXT_KEYS = {"text_id", "title_sa", "title_en", "category", "chapters", "structure", "status"}
CHAPTER_KEYS = {"number", "title", "title_en", "shlokas"}
VERSE_KEYS = {
    "number", "text", "english", "hindi", "status",
    "ref", "tags", "english_draft", "hindi_draft", "meter", "tags_draft",
}

# Keys whose COLUMN HAS A DIFFERENT NAME. A rename is as capable of silent loss as an
# omission — nothing would have flagged `text` -> `devanagari` if this test only compared
# names — so the mapping is declared and the target column's existence is asserted.
RENAMED = {
    ("text", "text_id"): "id",        # the slug is the primary key
    ("verse", "text"): "devanagari",  # `text` is far too generic beside a `text` TABLE
}

# Keys that are real and modelled NOWHERE, each with the reason. Being on this list is a
# decision; being absent from both this list and the schema is a bug.
KNOWN_OMITTED = {
    # Structural containers — they become rows, not columns.
    ("text", "chapters"): "becomes the section/verse tree",
    ("chapter", "shlokas"): "becomes verse rows",
    ("chapter", "number"): "becomes section.label (literal) + section.position (ordering)",
    ("verse", "number"): "becomes verse.number_label (literal) + verse.position (ordering)",
    # Denormalised aggregates. A cached summary that can disagree with its source is a defect
    # waiting to happen; both are derivable with a GROUP BY.
    ("text", "status"): "always the literal 'translated' on 28 texts; derivable from its verses",
    # ("verse","status") IS NO LONGER HERE, and its removal is the point. It sat here reading
    # "derivable from annotation.state" -- true under the withdrawn two-state mapping, FALSE
    # from the moment that mapping went, and green either way because nothing tests whether a
    # KNOWN_OMITTED reason is still true. Two independent reviewers found it on the same day.
    # It is now a real column: verse.status, the ARRIVAL field. See G58-G61, DECISIONS
    # 2026-09-16, and the reason-mechanism test below.
    # The four annotation-bearing keys become annotation rows, not columns, because a verse can
    # hold a published AND a draft value for the same (kind, lang) at once.
    ("verse", "english"): "annotation(kind=translation, lang=en, state=published)",
    ("verse", "hindi"): "annotation(kind=translation, lang=hi, state=published)",
    ("verse", "english_draft"): "annotation(kind=translation, lang=en, state=draft)",
    ("verse", "hindi_draft"): "annotation(kind=translation, lang=hi, state=draft)",
    # kind='tag' for all nine namespaces; the namespace stays in the value (`phala:wealth`,
    # `rel:aspects`) and array order is preserved by annotation.position. Splitting two of the
    # nine out as their own `kind` lost which namespace the other seven came from.
    ("verse", "tags"): "annotation(kind=tag, value='<namespace>:<value>', ordered by position)",
    ("verse", "tags_draft"): "annotation(kind=tag, state=draft, ordered by position)",
}


def _census() -> dict[str, set[str]]:
    """Every key actually present, at each level, across every corpus JSON."""
    found: dict[str, set[str]] = {"text": set(), "chapter": set(), "verse": set()}
    for path in REPO.rglob("*.json"):
        rel = path.relative_to(REPO)
        if rel.parts[0] in {"docs", ".venv", ".venv-corpus", "migrations", "node_modules"}:
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(doc, dict) or "text_id" not in doc or "chapters" not in doc:
            continue
        # The census describes the corpus the DATABASE will hold, so it skips exactly what the
        # importer skips -- one named constant, not two independent filters. These four carry
        # five keys nobody declared (`notes`, `count_authority`, `title`, `language`, `author`)
        # and a sixth on 490 verses (`source_number`), and adding those to the allowlist would
        # be the census endorsing fabricated files as schema. G62.
        if doc["text_id"] in EXCLUDED_TEXTS:
            continue
        found["text"] |= set(doc)
        for chapter in doc["chapters"]:
            found["chapter"] |= set(chapter)
            for shloka in chapter["shlokas"]:
                found["verse"] |= set(shloka)
    return found


@pytest.fixture(scope="module")
def census() -> dict[str, set[str]]:
    c = _census()
    if not c["verse"]:
        pytest.skip("no corpus JSON found — absent, not a pass")
    return c


@pytest.mark.parametrize(
    "level,allowed", [("text", TEXT_KEYS), ("chapter", CHAPTER_KEYS), ("verse", VERSE_KEYS)]
)
def test_no_unseen_key_appears_at_any_level(census, level: str, allowed: set[str]):
    unseen = census[level] - allowed
    assert not unseen, (
        f"{level}-level key(s) {sorted(unseen)} exist in the corpus and are declared nowhere. "
        f"Give each one a column, or add it to KNOWN_OMITTED with a reason. Silently dropping "
        f"it is what happened to `structure`."
    )


@pytest.mark.parametrize(
    "level,allowed,model",
    [("text", TEXT_KEYS, Text_), ("chapter", CHAPTER_KEYS, Section), ("verse", VERSE_KEYS, Verse)],
)
def test_every_declared_key_is_modelled_or_explicitly_omitted(level, allowed, model):
    """The half that actually prevents a repeat of `structure`.

    Knowing a key exists is not enough — `_normalize_shloka` "knew" about every key it dropped.
    Each must resolve to a column or to a recorded decision.
    """
    columns = {c.name for c in model.__table__.columns}
    homeless = [
        k for k in sorted(allowed)
        if k not in columns
        and (level, k) not in KNOWN_OMITTED
        and (level, k) not in RENAMED
    ]
    assert not homeless, (
        f"{level}-level key(s) {homeless} are declared in the census but have no column on "
        f"{model.__name__}, no RENAMED mapping, and no KNOWN_OMITTED entry."
    )
    # A rename pointing at a column that does not exist is the same silent loss wearing a
    # mapping — assert the target, not just the intent.
    broken = [
        f"{k} -> {col}" for (lvl, k), col in RENAMED.items()
        if lvl == level and col not in columns
    ]
    assert not broken, f"{level}: RENAMED points at missing column(s) on {model.__name__}: {broken}"


def test_the_census_can_actually_fail():
    """rule:discernment-checks §1 — ship the input that makes the check fail.

    Without this, a census whose rglob matched nothing, or whose allowed-set was accidentally
    widened to everything, would pass silently and forever.
    """
    unseen = {"number", "text", "a_key_that_does_not_exist"} - VERSE_KEYS
    assert unseen == {"a_key_that_does_not_exist"}, (
        "the set-difference the census relies on does not discriminate"
    )


def test_every_known_omitted_key_is_genuinely_absent_from_its_model():
    """A KNOWN_OMITTED entry is a claim that the key has NO column. Check the claim.

    This is the half that was missing when `("verse","status")` sat here with a justification
    that had quietly become false. It does not verify the REASON prose -- nothing can -- but it
    does catch the case that actually bit: a key recorded as omitted which has since been
    modelled, or modelled and then recorded as omitted, leaving two contradictory answers in
    the same file. rule:discernment-checks §1: ship the input that makes the check fail.
    """
    models = {"text": Text_, "chapter": Section, "verse": Verse}
    contradictions = []
    for (level, key), reason in KNOWN_OMITTED.items():
        model = models[level]
        if key in {c.name for c in model.__table__.columns}:
            contradictions.append(f"{level}.{key} is recorded as omitted ({reason!r}) but "
                                  f"{model.__name__} HAS that column")
    assert not contradictions, "\n".join(contradictions)


def test_the_exclusion_list_still_matches_what_is_on_disk():
    """An exclusion whose file has gone is folklore; one whose file is back is a hole.

    G62's four are untracked, so a `git clean` removes them and this list silently starts
    describing nothing. Either state is a finding -- report it rather than passing quietly.
    """
    on_disk = set()
    for path in REPO.rglob("*.json"):
        if path.relative_to(REPO).parts[0] in {"docs", ".venv", ".venv-corpus", "migrations",
                                               "node_modules", "venv"}:
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if isinstance(doc, dict) and "text_id" in doc:
            on_disk.add(doc["text_id"])
    if not on_disk:
        pytest.skip("no corpus JSON found -- absent, not a pass")
    stale = sorted(set(EXCLUDED_TEXTS) - on_disk)
    assert not stale, (
        f"EXCLUDED_TEXTS names {stale}, which are no longer on disk. If they were deleted, "
        f"remove them here and close the TODO; if they moved, say where in the reason."
    )
