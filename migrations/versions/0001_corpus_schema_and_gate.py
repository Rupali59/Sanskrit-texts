"""corpus schema, the published views, and the read-only API role

Revision ID: 0001_corpus_schema_and_gate
Revises:
Create Date: 2026-09-16

THE ROLE AND THE VIEWS ARE THE POINT OF THIS MIGRATION, not the tables.

docker-compose.yml creates exactly one role, the OWNER. That is deliberate: a single
POSTGRES_USER hands every consumer the owner credentials, and a table owner can re-grant past
any REVOKE and is not subject to RLS unless it is FORCEd. So a publication gate built on GRANT
is worth nothing if the application connects as owner. The read-only role is created HERE,
given SELECT on the published views and nothing at all on `annotation` / `annotation_revision`.

`tests/test_publication_gate.py` asserts all three halves: a draft's bytes reach no published
surface, the same bytes DO reach one once published (the negative control, without which the
first assertion is vacuous), and the API role cannot read the underlying tables even
deliberately.
"""

from __future__ import annotations

import os

import sqlalchemy as sa
from alembic import op

revision = "0001_corpus_schema_and_gate"
down_revision = None
branch_labels = None
depends_on = None

# Mirrors KNOWN_CATEGORIES in astroacharya/scripts/validate_corpus.py (21 members). The corpus
# uses 14 of them; the rest cover Youvan's scope so a shared validator run does not reject
# them. A real FK here closes the defect that file names at :41-43 -- category is an
# unvalidated string at ingest, so a typo silently mints a new one.
CATEGORIES = [
    "aranyaka", "brahmana", "dharmashastra", "jaimini", "kalpa", "mantra", "muhurta",
    "nadi", "nibandha", "parashari", "samhita", "siddhanta", "tantra", "upanishad",
    "upaveda_ayurveda", "upaveda_dhanurveda", "upaveda_gandharvaveda",
    "upaveda_sthapatyaveda", "veda_samhita", "vedanga_jyotisha", "vedanta",
]

# DELIBERATELY NOT MODELLED: a TEXT-level `status` key exists on 28 texts and is always
# the literal "translated". It is a denormalised summary of its own verses, derivable with
# a GROUP BY, and a cached aggregate that can disagree with its source is a defect waiting
# to happen. tests/test_key_census.py records it as known-and-omitted, not unseen.
API_ROLE = "corpus_api"
# T12/M2, 2026-09-16. Was a hardcoded literal, and because the CREATE below is guarded by
# IF NOT EXISTS it could never be rotated: the committed value was the password for the life
# of the role. Now env-driven, and ALTER ROLE runs unconditionally so setting the variable
# rotates an existing role rather than silently doing nothing.
#
# The fallback is the LOCAL DEVELOPMENT password and is deliberately still here: this database
# binds 127.0.0.1:5433 and `tests/conftest.py` needs a working default. A deployment sets
# CORPUS_API_PASSWORD; there is no scenario where this literal is a deployment credential.
API_PASSWORD = os.environ.get("CORPUS_API_PASSWORD", "corpus_api_local")


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column("name", sa.String(48), primary_key=True),
        sa.Column("note", sa.Text()),
    )
    op.bulk_insert(
        sa.table("category", sa.column("name", sa.String), sa.column("note", sa.Text)),
        [{"name": c, "note": None} for c in CATEGORIES],
    )

    op.create_table(
        "text",
        sa.Column("id", sa.String(64), primary_key=True),
        sa.Column("title_sa", sa.Text()),
        sa.Column("title_en", sa.Text()),
        sa.Column("category", sa.String(48), sa.ForeignKey("category.name", ondelete="RESTRICT")),
        sa.Column("structure", sa.dialects.postgresql.JSONB()),
        sa.Column("source_sha", sa.String(64)),
        # T7/D11: the Siromani parts. RESTRICT so deleting a parent work cannot orphan them.
        sa.Column("part_of", sa.String(64), sa.ForeignKey("text.id", ondelete="RESTRICT")),
    )
    op.create_index("ix_text_part_of", "text", ["part_of"])

    # T7/D10: the directory middle level as a facet table, not two columns on `text`.
    op.create_table(
        "text_facet",
        sa.Column("text_id", sa.String(64), sa.ForeignKey("text.id", ondelete="CASCADE"),
                  primary_key=True),
        sa.Column("kind", sa.String(16), primary_key=True),
        sa.Column("value", sa.String(64), primary_key=True),
        sa.CheckConstraint(
            "kind IN ('school','shakha','discipline','recension','veda')", name="ck_facet_kind"
        ),
    )
    op.create_index("ix_facet_kind_value", "text_facet", ["kind", "value"])

    op.create_table(
        "section",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("text_id", sa.String(64), sa.ForeignKey("text.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("parent_id", sa.BigInteger(), sa.ForeignKey("section.id", ondelete="CASCADE")),
        sa.Column("depth", sa.SmallInteger(), nullable=False),
        sa.Column("level_name", sa.String(32), nullable=False),
        sa.Column("label", sa.String(64), nullable=False),
        sa.Column("title", sa.Text()),
        # 2 chapters only, and saravali ch1's value is a structural caveat rather than a
        # translation. Kept because dropping it drops the caveat.
        sa.Column("title_en", sa.Text()),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.UniqueConstraint("text_id", "parent_id", "label", name="uq_section_sibling_label"),
        sa.CheckConstraint("depth >= 1", name="ck_section_depth_positive"),
    )
    # T1/G58: the UniqueConstraint above cannot constrain top-level sections -- NULL is never
    # equal to NULL -- so two chapters labelled "1" in one text committed silently.
    op.create_index(
        "uq_section_root_label", "section", ["text_id", "label"],
        unique=True, postgresql_where=sa.text("parent_id IS NULL"),
    )
    op.create_index("ix_section_text_id", "section", ["text_id"])
    op.create_index("ix_section_parent_id", "section", ["parent_id"])
    op.create_index("ix_section_text_depth", "section", ["text_id", "depth"])

    op.create_table(
        "verse",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("section_id", sa.BigInteger(), sa.ForeignKey("section.id", ondelete="CASCADE"),
                  nullable=False),
        # The literal printed label. Never parsed to sort -- `position` does ordering.
        sa.Column("number_label", sa.String(64), nullable=False),
        # Round-trip fidelity: 32 labels are digit-strings typed `str` in the source, which a
        # TEXT column cannot distinguish from an int. 4 texts mix both types.
        sa.Column("number_is_str", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("devanagari", sa.Text(), nullable=False),
        sa.Column("ref", sa.Text()),
        sa.Column("meter", sa.String(64)),
        # T5: the ARRIVAL field, NOT the editorial state. 69,813 verses carry both
        # translations while status reads 'untranslated'. export --fidelity needs it.
        sa.Column("status", sa.String(16)),
        # G8 turned from silent loss into a failed import: 70 verses are dropped today by
        # seed_texts.py's (chapter, shloka) dedupe, which logs a warning and continues.
        sa.UniqueConstraint("section_id", "number_label", name="uq_verse_label_in_section"),
        sa.UniqueConstraint("section_id", "position", name="uq_verse_position_in_section"),
    )
    op.create_index("ix_verse_section_id", "verse", ["section_id"])

    op.create_table(
        "annotation",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        sa.Column("verse_id", sa.BigInteger(), sa.ForeignKey("verse.id", ondelete="CASCADE"),
                  nullable=False),
        sa.Column("kind", sa.String(16), nullable=False),
        sa.Column("lang", sa.String(8)),
        sa.Column("value", sa.Text(), nullable=False),
        # Which JSON key this came from. UC1 lands `english` and `english_draft` both as
        # draft translations in `en`, so without this the two are indistinguishable and the
        # fidelity export cannot reproduce the source.
        sa.Column("source_field", sa.String(16)),
        # T9: tags are an ARRAY and an array has an order; without this the importer cannot
        # round-trip `tags`. NULL for translations, where ordering is meaningless.
        sa.Column("position", sa.Integer()),
        sa.Column("state", sa.String(16), nullable=False, server_default="draft"),
        sa.Column("current_revision_id", sa.BigInteger()),
        # M5/B3: two kinds. `phala` and `align` are TAG NAMESPACES (2 of 9), not kinds --
        # the namespace lives in the value as `prefix:value`, which is how the corpus writes it.
        sa.CheckConstraint("kind IN ('translation','tag')", name="ck_annotation_kind"),
        sa.CheckConstraint(
            "state IN ('draft','in_review','needs_revision','approved','superseded')",
            name="ck_annotation_state",
        ),
    )
    op.create_index("ix_annotation_verse_id", "annotation", ["verse_id"])
    # T7: the published view joins on (verse_id, state); the partial unique index below covers
    # only approved rows, so the draft side would scan without this.
    op.create_index("ix_annotation_verse_state", "annotation", ["verse_id", "state"])
    # PARTIAL unique: one PUBLISHED value per (verse, kind, lang). Drafts are unconstrained so
    # a pending edit can coexist with the live one -- 2,369 draft-bearing verses also carry a
    # populated english/hindi, and a total unique index would force the import to drop one side.
    # T6: predicate follows the state rename. 'published' is no longer a legal state, so
    # leaving it here would have made this index match ZERO rows -- a uniqueness constraint
    # that silently stops constraining, which is the failure class this schema exists to close.
    op.create_index(
        "uq_annotation_approved", "annotation", ["verse_id", "kind", "lang"],
        unique=True, postgresql_where=sa.text("state = 'approved'"),
    )

    op.create_table(
        "annotation_revision",
        sa.Column("id", sa.BigInteger(), primary_key=True),
        # T3/G60: RESTRICT. CASCADE here erased the provenance this table exists to keep.
        sa.Column("annotation_id", sa.BigInteger(),
                  sa.ForeignKey("annotation.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("value", sa.Text(), nullable=False),
        sa.Column("state", sa.String(16), nullable=False),
        sa.Column("author", sa.String(128)),
        sa.Column("method", sa.String(16), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"),
                  nullable=False),
        sa.Column("supersedes_id", sa.BigInteger(),
                  sa.ForeignKey("annotation_revision.id", ondelete="SET NULL")),
        sa.Column("note", sa.Text()),
        sa.CheckConstraint("method IN ('human','machine','matcher')", name="ck_revision_method"),
        sa.CheckConstraint(
            "state IN ('draft','in_review','needs_revision','approved','superseded')",
            name="ck_revision_state",
        ),
    )
    op.create_index("ix_revision_annotation_id", "annotation_revision", ["annotation_id"])
    op.create_index("ix_revision_annotation_created", "annotation_revision",
                    ["annotation_id", "created_at"])

    # ---- append-only, enforced ---------------------------------------------------------
    # T3/G60. "NEVER updated, never deleted" was a docstring; the owner role holds full
    # UPDATE/DELETE. A trigger is the only thing that makes it a property of the database.
    op.execute("""
        CREATE OR REPLACE FUNCTION annotation_revision_append_only() RETURNS trigger AS $fn$
        BEGIN
            RAISE EXCEPTION
                'annotation_revision is append-only; % is not permitted', TG_OP
                USING ERRCODE = '23514';
        END;
        $fn$ LANGUAGE plpgsql;
    """)
    op.execute("""
        CREATE TRIGGER trg_annotation_revision_append_only
        BEFORE UPDATE OR DELETE ON annotation_revision
        FOR EACH ROW EXECUTE FUNCTION annotation_revision_append_only();
    """)

    # ---- the published surface -------------------------------------------------------
    # A VIEW over state='approved'. `annotation` is joined only through this filter, so a
    # draft has no path to a consumer: not a column the API forgets to exclude, an absent row.
    op.execute("""
        CREATE VIEW published_text AS
        SELECT t.id, t.title_sa, t.title_en, t.category, t.structure
        FROM text t
    """)
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

    # ---- the role ---------------------------------------------------------------------
    # Created here rather than in compose, so the application can never hold the owner DSN.
    op.execute(f"""
        DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '{API_ROLE}') THEN
                CREATE ROLE {API_ROLE} LOGIN PASSWORD '{API_PASSWORD}';
            END IF;
        END $$;
    """)
    # Unconditional, so CORPUS_API_PASSWORD actually rotates an existing role. With only the
    # IF NOT EXISTS above, a changed variable was silently ignored on every run after the first.
    op.execute(f"ALTER ROLE {API_ROLE} WITH LOGIN PASSWORD '{API_PASSWORD}'")
    # T12/M2: current_database(), not a hardcoded name. `GRANT CONNECT ON DATABASE` takes a
    # literal identifier, so it goes through format() inside a DO block. The hardcoded name
    # made this migration fail on any other database -- including the `_test` database the
    # TRUNCATE guard wants and any CI service DB -- and the failure read as broken tooling
    # rather than as a misconfiguration.
    op.execute(
        f"""
        DO $$
        BEGIN
            EXECUTE format('GRANT CONNECT ON DATABASE %I TO {API_ROLE}', current_database());
        END $$;
    """
    )
    op.execute(f"GRANT USAGE ON SCHEMA public TO {API_ROLE}")
    # SELECT on the views only. Nothing on annotation or annotation_revision -- the revision
    # table holds every draft value ever written, so a grant there leaks more than annotation.
    op.execute(f"GRANT SELECT ON published_text, published_verse TO {API_ROLE}")
    # T4/M3, 2026-09-16: THIS LINE CANNOT FAIL AND IS NOT A CHECK. Default-privilege REVOKE
    # only removes a default GRANT for objects created after it runs, and no default grant to
    # corpus_api exists for it to remove -- this migration never issued one, and Postgres does
    # not hand a new table's privileges to anyone but its owner unless told to. So this
    # statement executes, changes nothing, and reads as protection while defending nothing.
    # `rule:discernment-checks` §1: a check that cannot fail is worse than no check.
    #
    # The real hazard -- a FUTURE migration writing an explicit `GRANT ... TO corpus_api` or
    # `TO PUBLIC` -- is caught by
    # tests/test_grants_and_views.py::test_corpus_api_grant_set_is_exactly_select_on_published_views,
    # which reads information_schema.role_table_grants and asserts the grant set is exactly
    # `{published_text: SELECT, published_verse: SELECT}`, derived from the schema rather than
    # a hardcoded list. THAT test is the real check; this line is kept only because 0001 is
    # committed and shared, so removing it would change a migration someone has already run.
    op.execute(
        f"ALTER DEFAULT PRIVILEGES IN SCHEMA public REVOKE ALL ON TABLES FROM {API_ROLE}"
    )


def downgrade() -> None:
    op.execute(f"REVOKE ALL ON published_text, published_verse FROM {API_ROLE}")
    op.execute("DROP TRIGGER IF EXISTS trg_annotation_revision_append_only ON annotation_revision")
    op.execute("DROP FUNCTION IF EXISTS annotation_revision_append_only()")
    op.execute("DROP VIEW IF EXISTS published_verse")
    op.execute("DROP VIEW IF EXISTS published_text")
    # IF EXISTS, deliberately. `0001` is amended in place while it holds no real data, so a
    # downgrade routinely runs against a database created by an EARLIER draft of this same
    # revision -- and `op.drop_table` on a table that draft never created aborts mid-way,
    # leaving a half-dropped schema that neither upgrades nor downgrades. Verified 2026-09-16:
    # adding `text_facet` here broke `alembic downgrade base` against the previous draft.
    for t in ("annotation_revision", "annotation", "verse", "section", "text_facet", "text",
              "category"):
        op.execute(f"DROP TABLE IF EXISTS {t}")
    # The role is intentionally NOT dropped: it may own grants in other databases on this
    # cluster, and dropping a role out from under them fails in a way that is hard to read.
