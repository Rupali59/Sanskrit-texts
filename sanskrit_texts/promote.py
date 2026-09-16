"""Move annotations through the editorial lifecycle. The gate's legitimate door.

WHY THIS EXISTS AT ALL, AND WHY IT IS AUDITED RATHER THAN FORBIDDEN.

The design argues -- correctly -- that withholding unreviewed text creates pressure toward a
bulk `UPDATE ... SET state='approved'`, an operation indistinguishable from legitimate use.
The conclusion usually drawn is "forbid bulk promotion". That is the wrong conclusion. There
are 209,600 draft annotations and a real backlog of already-curated content behind them
(`scripts/apply_translations.py` is ~33 KB of hand-authored Suryasiddhanta and Goladhyaya
Hindi; thousands of verses carry an `english` byte-identical to their prior `english_draft`,
which is a legitimate review outcome -- the draft was read and accepted unchanged).

Forbidding bulk while offering no path means the first person with real work to land reaches
for psql. **An audited bulk path is the defense.** Every promotion here writes an
`annotation_revision` naming a human and a method, and that table is append-only in the
database (a BEFORE UPDATE OR DELETE trigger, G60), so the record cannot be tidied away later.

THE ONE RULE THAT DOES NOT BEND: `approved` REQUIRES A NAMED HUMAN. Not a flag, not a default,
not an env var. This is the whole reason D9's `translated -> published` mapping was withdrawn
-- it would have asserted a review of 55,942 rows that nobody performed, inferred from a field
the corpus uses as an arrival date.

    draft ──> in_review ──> approved
      ^            │            │
      └── needs_revision        └──> superseded  (when a later revision replaces it)
"""

from __future__ import annotations

import argparse
import os
import sys

import sqlalchemy as sa

# Who may move where. `approved` is reachable from `in_review` OR straight from `draft` --
# a single reviewer accepting a draft in one sitting is the common case and pretending
# otherwise just invites people to route around the tool.
TRANSITIONS: dict[str, set[str]] = {
    "draft": {"in_review", "approved", "needs_revision"},
    "in_review": {"approved", "needs_revision", "draft"},
    "needs_revision": {"draft", "in_review"},
    "approved": {"superseded", "needs_revision"},
    "superseded": set(),
}

# Only a human may put something in front of a reader. `machine` and `matcher` exist for
# import and tooling; neither can reach `approved`.
HUMAN_ONLY_STATES = {"approved"}
METHODS = ("human", "machine", "matcher")


class PromotionRefused(RuntimeError):
    """Raised instead of silently doing nothing, so a refusal is never mistaken for a no-op."""


def promote(
    conn: sa.Connection,
    *,
    text_id: str | None = None,
    verse_label: str | None = None,
    lang: str | None = None,
    kind: str | None = None,
    to_state: str,
    author: str | None,
    method: str = "human",
    note: str | None = None,
) -> int:
    """Move every matching annotation to `to_state`. Returns the number moved."""
    if to_state not in TRANSITIONS:
        raise PromotionRefused(f"unknown state {to_state!r}; known: {sorted(TRANSITIONS)}")
    if method not in METHODS:
        raise PromotionRefused(f"unknown method {method!r}; known: {list(METHODS)}")
    if to_state in HUMAN_ONLY_STATES:
        if not (author or "").strip():
            raise PromotionRefused(
                f"{to_state!r} requires --author: a named human, not a tool. This is the rule "
                f"the whole publication gate rests on -- nothing reaches a reader because a "
                f"script decided it was ready."
            )
        if method != "human":
            raise PromotionRefused(
                f"{to_state!r} requires --method human; got {method!r}. A matcher can propose, "
                f"it cannot approve."
            )

    where = ["a.state <> :to"]
    params: dict[str, object] = {"to": to_state}
    if text_id:
        where.append("s.text_id = :text_id")
        params["text_id"] = text_id
    if verse_label:
        where.append("v.number_label = :vl")
        params["vl"] = verse_label
    if lang:
        where.append("a.lang = :lang")
        params["lang"] = lang
    if kind:
        where.append("a.kind = :kind")
        params["kind"] = kind

    rows = conn.execute(
        sa.text(
            "SELECT a.id, a.state, a.value, a.verse_id, a.kind, a.lang, a.source_field"
            " FROM annotation a"
            " JOIN verse v ON v.id = a.verse_id JOIN section s ON s.id = v.section_id"
            " WHERE " + " AND ".join(where) + " ORDER BY a.id"
        ),
        params,
    ).mappings().all()
    if not rows:
        raise PromotionRefused(
            "no annotation matched -- refusing silently would look identical to success"
        )

    illegal = {r["state"] for r in rows if to_state not in TRANSITIONS[r["state"]]}
    if illegal:
        raise PromotionRefused(
            f"illegal transition to {to_state!r} from {sorted(illegal)}. "
            f"Allowed into {to_state!r}: "
            f"{sorted(s for s, t in TRANSITIONS.items() if to_state in t)}"
        )

    # Two drafts of the same (verse, kind, lang) cannot both be approved -- the partial
    # unique index says one. Reaching the constraint and aborting would be correct but
    # opaque; naming the clash is the useful behaviour. A verse commonly holds BOTH a served
    # value and its draft (2,369 do), so this is the ordinary case, not an edge one.
    if to_state == "approved":
        seen: dict[tuple, list] = {}
        for r in rows:
            seen.setdefault((r["verse_id"], r["kind"], r["lang"]), []).append(r)
        clashes = {k: v for k, v in seen.items() if len(v) > 1}
        if clashes:
            key, group = next(iter(clashes.items()))
            fields = ", ".join(sorted(str(g["source_field"]) for g in group))
            raise PromotionRefused(
                f"{len(clashes)} verse(s) would end up with more than one approved value for "
                f"the same (verse, kind, lang) -- only one is permitted. First clash: "
                f"verse_id={key[0]} kind={key[1]!r} lang={key[2]!r}, {len(group)} candidates "
                f"from {fields}. Narrow the selection (--verse, --kind, --lang) so exactly one "
                f"wins; approving is a choice between them, not a bulk operation."
            )

    ids = [r["id"] for r in rows]
    # Supersede any annotation already approved for the same (verse, kind, lang): the partial
    # unique index permits exactly one, so this is not tidiness -- without it the UPDATE below
    # violates the constraint and the whole promotion aborts.
    if to_state == "approved":
        conn.execute(
            sa.text(
                "UPDATE annotation SET state = 'superseded' WHERE state = 'approved'"
                " AND id <> ALL(:ids) AND (verse_id, kind, COALESCE(lang, '')) IN"
                " (SELECT verse_id, kind, COALESCE(lang, '') FROM annotation"
                "  WHERE id = ANY(:ids))"
            ),
            {"ids": ids},
        )
    conn.execute(
        sa.text("UPDATE annotation SET state = :to WHERE id = ANY(:ids)"),
        {"to": to_state, "ids": ids},
    )
    conn.execute(
        sa.insert(sa.table(
            "annotation_revision",
            sa.column("annotation_id"), sa.column("value"), sa.column("state"),
            sa.column("author"), sa.column("method"), sa.column("note"),
        )),
        [{"annotation_id": r["id"], "value": r["value"], "state": to_state,
          "author": author, "method": method,
          "note": note or f"{r['state']} -> {to_state}"} for r in rows],
    )
    return len(ids)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--dsn", default=None, help="defaults to $CORPUS_OWNER_DSN")
    ap.add_argument("--to", required=True, choices=sorted(TRANSITIONS),
                    help="target state. `approved` requires --author and --method human.")
    ap.add_argument("--author", help="the named human accountable for this review")
    ap.add_argument("--method", default="human", choices=METHODS)
    ap.add_argument("--note", help="free text recorded on every revision written")
    ap.add_argument("--text", help="restrict to one text_id")
    ap.add_argument("--verse", help="restrict to one verse number_label")
    ap.add_argument("--lang", help="restrict to one language")
    ap.add_argument("--kind", help="restrict to one annotation kind")
    ap.add_argument("--dry-run", action="store_true",
                    help="run the real UPDATE and roll it back, reporting the count")
    args = ap.parse_args(argv)

    dsn = args.dsn or os.environ.get("CORPUS_OWNER_DSN")
    if not dsn:
        print("no DSN: pass --dsn or set CORPUS_OWNER_DSN", file=sys.stderr)
        return 2

    engine = sa.create_engine(dsn, future=True)
    with engine.connect() as conn:
        trans = conn.begin()
        try:
            n = promote(conn, text_id=args.text, verse_label=args.verse, lang=args.lang,
                        kind=args.kind, to_state=args.to, author=args.author,
                        method=args.method, note=args.note)
        except PromotionRefused as exc:
            trans.rollback()
            print(f"REFUSED: {exc}", file=sys.stderr)
            return 1
        if args.dry_run:
            trans.rollback()
            print(f"DRY RUN: would move {n:,} annotation(s) to {args.to!r} (rolled back)")
        else:
            trans.commit()
            who = f" by {args.author!r}" if args.author else ""
            print(f"moved {n:,} annotation(s) to {args.to!r}{who}; "
                  f"{n:,} revision(s) recorded")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
