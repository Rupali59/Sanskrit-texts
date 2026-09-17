"""confidence markers: a machine CHECK layer and human REVIEW confidence

Revision ID: 0003_confidence_markers
Revises: 0002_text_status
Create Date: 2026-09-17

T6 (DECISIONS.md 2026-09-17), Phase A only: translations and tags. Two layers, deliberately
different tables, deliberately unable to influence each other automatically.

THE MACHINE LAYER, `annotation_check`. One row per annotation, replaced wholesale on every
recompute -- the primary key IS `annotation_id`, not a surrogate id. A check is recomputable
state, never provenance, which is why its FK is ON DELETE CASCADE where
`annotation_revision`'s is deliberately RESTRICT (G60): deleting the annotation may take its
check with it without losing anything G60 exists to protect. G55 is why `level` can never
assert a value is right: every signal `sanskrit_texts/checks.py` computes measures presence
and shape, never correctness, so the best it can ever report is `no-defect-found` -- never
"high", never "verified". `unchecked` is legal for the CHECK constraint's completeness only;
the checker never emits it -- a row simply absent from this table IS "never checked".

THE HUMAN LAYER, `annotation_revision.confidence`. NULL everywhere except `approved`:
`ck_revision_approved_has_confidence` makes that a database fact, not a promise `promote.py`'s
argparse enforces alone. `override_reason` records why a human approved something an
automated check flagged `fails` -- required by `promote.py`, not enforced here, because "was
this checked `fails`" is a fact in a DIFFERENT table this constraint cannot see.

THE PUBLISHED SURFACE. `published_verse` gets two columns APPENDED at the end -- Postgres
requires CREATE OR REPLACE VIEW to keep every existing column's name, position and type
unchanged, and appending via replace (rather than DROP + CREATE) is what lets `corpus_api`'s
existing SELECT grant survive without a re-GRANT. `published_text` carries no per-verse
annotation, so Phase A does not touch it -- structure/count confidence is Phase C, not this
migration. This migration issues no GRANT at all, so
`tests/test_grants_and_views.py::test_corpus_api_grant_set_is_exactly_select_on_published_views`
needs no change -- the grant set stays exactly `{published_text: SELECT, published_verse:
SELECT}`.

0001 and 0002 are pushed and shared -- amend neither; this is a new revision.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0003_confidence_markers"
down_revision = "0002_text_status"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "annotation_check",
        # PK is the annotation, not a surrogate: a check is recomputable state about ONE
        # annotation, never a history -- recomputing replaces this row in place.
        sa.Column(
            "annotation_id",
            sa.BigInteger(),
            sa.ForeignKey("annotation.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column("level", sa.Text(), nullable=False),
        sa.Column(
            "reasons", sa.ARRAY(sa.Text()), nullable=False,
            server_default=sa.text("'{}'::text[]"),
        ),
        sa.Column("checker_version", sa.Text(), nullable=False),
        sa.Column(
            "checked_at", sa.DateTime(timezone=True), nullable=False,
            server_default=sa.text("now()"),
        ),
        sa.CheckConstraint(
            "level IN ('fails','suspect','no-defect-found','unchecked')",
            name="ck_annotation_check_level",
        ),
    )

    # Human confidence, and the ONE rule that does not bend: approved requires it. Nullable
    # elsewhere -- confidence is meaningless for draft/in_review/needs_revision/superseded.
    # There are zero approved rows today (DECISIONS.md 2026-09-16/17), so adding this CHECK
    # has nothing existing to violate.
    op.add_column("annotation_revision", sa.Column("confidence", sa.Text(), nullable=True))
    op.add_column("annotation_revision", sa.Column("override_reason", sa.Text(), nullable=True))
    op.create_check_constraint(
        "ck_revision_confidence", "annotation_revision",
        "confidence IN ('certain','probable','tentative')",
    )
    op.create_check_constraint(
        "ck_revision_approved_has_confidence", "annotation_revision",
        "state <> 'approved' OR confidence IS NOT NULL",
    )

    # published_verse, columns appended at the END -- see module docstring for why
    # CREATE OR REPLACE (not DROP + CREATE) is what keeps the corpus_api grant intact. Every
    # column above `confidence` repeats 0001's definition verbatim, byte for byte.
    op.execute("""
        CREATE OR REPLACE VIEW published_verse AS
        SELECT v.id            AS verse_id,
               t.id            AS text_id,
               s.id            AS section_id,
               s.level_name,
               s.label         AS section_label,
               v.number_label,
               v.position,
               v.devanagari,
               v.ref,
               v.meter,
               a.kind,
               a.lang,
               a.value,
               -- The confidence of the revision that MADE this annotation approved -- not
               -- just any revision on it. An annotation can carry an earlier 'approved'
               -- revision from before a needs_revision/re-approve cycle, so this picks the
               -- most recent 'approved' revision, matching the row a.state='approved' means
               -- right now. NULL for a NULL annotation (a.id IS NULL correlates to nothing).
               (SELECT ar.confidence FROM annotation_revision ar
                 WHERE ar.annotation_id = a.id AND ar.state = 'approved'
                 ORDER BY ar.created_at DESC LIMIT 1) AS confidence,
               ac.level        AS check_level
        FROM verse v
        JOIN section s ON s.id = v.section_id
        JOIN text    t ON t.id = s.text_id
        LEFT JOIN annotation a
               ON a.verse_id = v.id
              AND a.state = 'approved'
        LEFT JOIN annotation_check ac ON ac.annotation_id = a.id
    """)


def downgrade() -> None:
    # CREATE OR REPLACE VIEW cannot drop trailing columns -- Postgres requires DROP + CREATE
    # for that, unlike the append-only case upgrade() relies on. That means the grant is lost
    # and must be reissued so a partial downgrade (to 0002) leaves corpus_api exactly as 0001
    # left it.
    op.execute("DROP VIEW IF EXISTS published_verse")
    op.execute("""
        CREATE VIEW published_verse AS
        SELECT v.id            AS verse_id,
               t.id            AS text_id,
               s.id            AS section_id,
               s.level_name,
               s.label         AS section_label,
               v.number_label,
               v.position,
               v.devanagari,
               v.ref,
               v.meter,
               a.kind,
               a.lang,
               a.value
        FROM verse v
        JOIN section s ON s.id = v.section_id
        JOIN text    t ON t.id = s.text_id
        LEFT JOIN annotation a
               ON a.verse_id = v.id
              AND a.state = 'approved'
    """)
    op.execute("GRANT SELECT ON published_verse TO corpus_api")

    op.drop_constraint("ck_revision_approved_has_confidence", "annotation_revision", type_="check")
    op.drop_constraint("ck_revision_confidence", "annotation_revision", type_="check")
    op.drop_column("annotation_revision", "override_reason")
    op.drop_column("annotation_revision", "confidence")
    op.drop_table("annotation_check")
