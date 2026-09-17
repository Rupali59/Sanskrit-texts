"""The MACHINE layer of T6's confidence markers -- Phase A: translations and tags.

G55 IS THE CONSTRAINT THAT SHAPES EVERYTHING HERE. A Devanagari ratio, a length comparison, an
NFC check -- every signal below measures presence and shape, never correctness, and none of
them can ever tell you a translation is RIGHT. So the best a check can report is
`no-defect-found`: a measured absence of a known defect shape, not a verdict. NEVER name a
level "high" or "verified" -- that is the exact overreach G55 records Prasna Marga scoring
81.4% Devanagari, 0 ASCII, and being unreadable at the glyph level throughout.

TWO PURE FUNCTIONS, ONE PER KIND. `check_translation` and `check_tag` each take only the
fields of ONE annotation (plus, for a translation, its verse's Devanagari) and return
`(level, reasons)` -- same inputs, same output, every run, so they need no database or clock
to unit-test. `duplicate-tag` is the one reason that cannot be a fact about a single
annotation in isolation: it is a fact about SIBLING tags on the same (verse, state), so it is
computed separately, by `find_duplicate_tag_ids`, over a whole group -- `compute_checks` is
what assembles the two.

WHAT THIS DELIBERATELY DOES NOT DO. It does not attempt G56's missed-tag detection
(`vowel-initial-root`, `excluded-root`, `no-lexicon-entry`) -- a MISSING tag is a fact about the
VERSE (nothing was tagged that should have been), not about an annotation that exists. That is
Phase B's `verse_check`/`verification` surface, not this one. And it never writes `state`: see
`tests/test_confidence.py`'s invariant test -- a check result is read-only with respect to the
editorial lifecycle, by construction, because nothing in this module imports or touches
`annotation.state`.

CHECKER_VERSION IS RECORDED ON EVERY ROW so a changed result under a later version is
traceable rather than looking like an unexplained flip -- see `docs/DATABASE.md`.
"""

from __future__ import annotations

import argparse
import collections
import os
import re
import sys
import unicodedata
from collections.abc import Iterable, Sequence
from typing import Any

import sqlalchemy as sa

CHECKER_VERSION = "1"

LEVELS = ("fails", "suspect", "no-defect-found", "unchecked")
_SEVERITY = {"no-defect-found": 0, "unchecked": 0, "suspect": 1, "fails": 2}

# The nine tag namespaces measured in DECISIONS.md 2026-09-16 (M5/B3): rel 6,019 · graha 2,070
# · bhava 1,805 · entity 1,318 · mahadasha 690 · rashi 509 · phala 475 · chain 271 · align 210.
# `phala`/`align` were once modelled as annotation KINDS and demoted -- see
# models.py's ANNOTATION_KINDS comment -- they remain valid tag NAMESPACES here.
TAG_NAMESPACES = frozenset(
    {"graha", "rashi", "bhava", "entity", "rel", "chain", "mahadasha", "phala", "align"}
)

_TEMPLATE_PREFIX = re.compile(r"^Classical text translation of [^:]+: ")
_LATIN_LETTER = re.compile(r"[A-Za-z]")
# ns:value. Lowercase (+ underscore, for a namespace not yet in TAG_NAMESPACES) so a malformed
# shape and an unknown namespace are two different, separately reported facts.
_TAG_SHAPE = re.compile(r"^([a-z_]+):(.+)$")

# Devanagari block, checked by direct code-point range rather than a `\w`/`\d`-family regex
# class -- G17 records `\d` matching Devanagari digits; the same family of surprise applies to
# `\w`. A literal range comparison has no such ambiguity.
_DEVANAGARI_LOW = "ऀ"
_DEVANAGARI_HIGH = "ॿ"


def _is_devanagari(ch: str) -> bool:
    return _DEVANAGARI_LOW <= ch <= _DEVANAGARI_HIGH


def _devanagari_share(value: str) -> float:
    """Devanagari characters as a share of NON-SPACE characters in `value`. A ratio, never a
    raw count -- G55's whole point is that a count alone answers "how much", never "how much
    of the RIGHT thing"."""
    body = [c for c in value if not c.isspace()]
    if not body:
        return 0.0
    return sum(1 for c in body if _is_devanagari(c)) / len(body)


def add_reason(level: str, reasons: list[str], reason: str, reason_level: str) -> tuple[str, list[str]]:
    """Fold one more (reason, level) into an existing result, keeping the MORE severe level and
    the union of reasons. Used to merge `duplicate-tag` -- a fact about siblings -- into a
    result `check_tag` already computed for a single annotation. Never downgrades: a `fails`
    annotation stays `fails` even if the only new fact is a `suspect`-level one.
    """
    merged_reasons = sorted(set(reasons) | {reason})
    merged_level = level if _SEVERITY[level] >= _SEVERITY[reason_level] else reason_level
    return merged_level, merged_reasons


def check_translation(lang: str, value: str, devanagari: str) -> tuple[str, list[str]]:
    """One translation annotation's value, checked against its verse's Devanagari. Pure: the
    caller supplies `checked_at`/`checker_version`, not this function, so it needs no clock and
    no database to test.

    Reasons, each independently detectable and jointly exhaustive of what this function can see:

      template-prefix  fails    value starts "Classical text translation of X: "
      sanskrit-echo     fails    en: >30% of value's non-space chars are Devanagari
                                 hi: value equals the verse's Sanskrit, or contains its first
                                     40 characters
      wrong-script      fails    en: zero Latin letters / hi: zero Devanagari characters
      too-short         suspect  value is under 30% of the Sanskrit's length, when the
                                 Sanskrit itself is over 40 characters (too short to be
                                 meaningful is only a signal once there is enough Sanskrit to
                                 be short RELATIVE to)
      not-nfc           suspect  unicodedata.normalize("NFC", value) != value

    `fails` beats `suspect` beats `no-defect-found` -- see `add_reason`'s severity order.
    """
    reasons: list[str] = []
    fails: set[str] = set()
    suspects: set[str] = set()

    if _TEMPLATE_PREFIX.match(value):
        fails.add("template-prefix")

    stripped_value = value.strip()
    stripped_dev = devanagari.strip()

    if lang == "en":
        if _devanagari_share(value) > 0.30:
            fails.add("sanskrit-echo")
        if not _LATIN_LETTER.search(value):
            fails.add("wrong-script")
    elif lang == "hi":
        if stripped_dev and (stripped_value == stripped_dev or stripped_dev[:40] in value):
            fails.add("sanskrit-echo")
        if not any(_is_devanagari(c) for c in value):
            fails.add("wrong-script")

    if len(stripped_dev) > 40 and len(stripped_value) < 0.3 * len(stripped_dev):
        suspects.add("too-short")

    if unicodedata.normalize("NFC", value) != value:
        suspects.add("not-nfc")

    reasons = sorted(fails | suspects)
    if fails:
        level = "fails"
    elif suspects:
        level = "suspect"
    else:
        level = "no-defect-found"
    return level, reasons


def check_tag(value: str) -> tuple[str, list[str]]:
    """One tag annotation's value, structurally. Pure -- see `check_translation`'s docstring.

      malformed-tag      fails    value is not shaped `ns:value` (lowercase namespace, colon,
                                   non-empty remainder)
      unknown-namespace  fails    the namespace is not one of TAG_NAMESPACES

    Does NOT attempt `duplicate-tag` -- that is a fact about SIBLING tags on the same
    (verse, state), not about this one value in isolation; see `find_duplicate_tag_ids`.

    Does NOT attempt G56's missed-tag detection (a vowel-initial root like `अष्टम` vanishing
    at a sandhi seam so `bhava:8` never gets written at all). A MISSING tag is a fact about the
    VERSE, not about an annotation that exists to be checked -- that is Phase B's
    `verse_check`, not this module.
    """
    reasons: list[str] = []
    m = _TAG_SHAPE.match(value)
    if not m:
        reasons.append("malformed-tag")
    elif m.group(1) not in TAG_NAMESPACES:
        reasons.append("unknown-namespace")

    level = "fails" if reasons else "no-defect-found"
    return level, reasons


def find_duplicate_tag_ids(rows: Sequence[tuple[int, str]]) -> set[int]:
    """IDs among `rows` (annotation_id, value) whose value occurs more than once.

    `rows` must already be scoped to ONE (verse_id, state) group -- `compute_checks` is what
    groups before calling this; a duplicate across two different verses, or a draft beside an
    already-approved value, is not the shape this reason names.
    """
    counts: dict[str, int] = collections.Counter(value for _aid, value in rows)
    return {aid for aid, value in rows if counts[value] > 1}


AnnotationRow = dict[str, Any]  # annotation_id, verse_id, kind, lang, value, state, devanagari
CheckResult = tuple[str, list[str]]


def compute_checks(rows: Iterable[AnnotationRow]) -> dict[int, CheckResult]:
    """Check every row, then fold in `duplicate-tag` per (verse_id, state) group.

    Each row must carry `annotation_id`, `verse_id`, `kind` ('translation' or 'tag'), `lang`,
    `value`, `state`, and (for a translation) `devanagari`. Returns {annotation_id: (level,
    reasons)} -- never writes anywhere; the caller (`upsert_checks`, or a test) decides what to
    do with the result, which is exactly what keeps this function's determinism testable
    without a database.
    """
    results: dict[int, CheckResult] = {}
    tag_groups: dict[tuple[int, str], list[tuple[int, str]]] = collections.defaultdict(list)

    for row in rows:
        aid = row["annotation_id"]
        kind = row["kind"]
        if kind == "translation":
            results[aid] = check_translation(row["lang"], row["value"], row["devanagari"])
        elif kind == "tag":
            results[aid] = check_tag(row["value"])
            tag_groups[(row["verse_id"], row["state"])].append((aid, row["value"]))
        else:
            raise ValueError(f"unknown annotation kind {kind!r} for annotation_id={aid}")

    for group in tag_groups.values():
        for aid in find_duplicate_tag_ids(group):
            level, reasons = results[aid]
            results[aid] = add_reason(level, reasons, "duplicate-tag", "suspect")

    return results


def iter_annotation_rows(conn: sa.Connection, text_ids: Sequence[str] | None = None) -> list[AnnotationRow]:
    """Every annotation eligible for a check, joined to its verse's Devanagari.

    Not scoped by `state` -- a draft is exactly what most needs checking, and nothing here
    reads or writes `annotation.state` (the invariant `tests/test_confidence.py` pins).
    """
    where = ""
    params: dict[str, object] = {}
    if text_ids:
        where = " WHERE s.text_id = ANY(:text_ids)"
        params["text_ids"] = list(text_ids)
    rows = conn.execute(
        sa.text(
            "SELECT a.id AS annotation_id, a.verse_id, a.kind, a.lang, a.value, a.state,"
            " v.devanagari"
            " FROM annotation a"
            " JOIN verse v ON v.id = a.verse_id"
            " JOIN section s ON s.id = v.section_id"
            + where
            + " ORDER BY a.id"
        ),
        params,
    ).mappings().all()
    return [dict(r) for r in rows]


def upsert_checks(conn: sa.Connection, results: dict[int, CheckResult]) -> None:
    """Write every result to `annotation_check`, replacing whatever row was there.

    `checked_at` is always `now()` on write, so two runs a moment apart are NOT byte-identical
    on that one column -- `tests/test_confidence.py`'s idempotence test compares every other
    column, which is the property this function actually promises.
    """
    if not results:
        return
    conn.execute(
        sa.text(
            "INSERT INTO annotation_check (annotation_id, level, reasons, checker_version,"
            " checked_at)"
            " VALUES (:annotation_id, :level, :reasons, :checker_version, now())"
            " ON CONFLICT (annotation_id) DO UPDATE SET"
            "   level = EXCLUDED.level,"
            "   reasons = EXCLUDED.reasons,"
            "   checker_version = EXCLUDED.checker_version,"
            "   checked_at = EXCLUDED.checked_at"
        ),
        [
            {
                "annotation_id": aid,
                "level": level,
                "reasons": reasons,
                "checker_version": CHECKER_VERSION,
            }
            for aid, (level, reasons) in results.items()
        ],
    )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dsn", default=None, help="defaults to $CORPUS_OWNER_DSN")
    ap.add_argument(
        "--text", action="append", dest="texts", metavar="SLUG",
        help="restrict to this text_id (repeatable); default: every text",
    )
    args = ap.parse_args(argv)

    dsn = args.dsn or os.environ.get("CORPUS_OWNER_DSN")
    if not dsn:
        print("no DSN: pass --dsn or set CORPUS_OWNER_DSN", file=sys.stderr)
        return 2

    engine = sa.create_engine(dsn, future=True)
    with engine.begin() as conn:
        rows = iter_annotation_rows(conn, args.texts)
        results = compute_checks(rows)
        upsert_checks(conn, results)

    level_counts = collections.Counter(level for level, _ in results.values())
    reason_counts: collections.Counter[str] = collections.Counter()
    for _level, reasons in results.values():
        reason_counts.update(reasons)

    print(f"checked {len(results):,} annotation(s), checker_version={CHECKER_VERSION!r}")
    for level in LEVELS:
        if level_counts[level]:
            print(f"  {level}: {level_counts[level]:,}")
    for reason, n in sorted(reason_counts.items()):
        print(f"    {reason}: {n:,}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
