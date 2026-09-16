"""SQLAlchemy 2.0 models — what is STORED.

This is one of two model layers and they are deliberately different classes. Pydantic in
`schema.py` owns what LEAVES the building. SQLModel was rejected precisely because it makes
them one class, and one class is how a storage concern (an ingest allowlist) became an
editorial policy (G50).

THREE IDEAS CARRY THE DESIGN.

**Identity != citation != ordering.** `verse.number_label` is the literal string the edition
prints — `"27 1/2"`, `"63अ"`, `"3.2.11"`, `"41-2"` — and `verse.position` is a plain integer
used only for ordering. Nothing ever parses a label to sort. `astroacharya`'s
`texts_repo.py:82` sorts verses IN PYTHON today because its Mongo key is int-or-str; that is
the defect this separation removes.

**`section` is a tree, and a RAGGED one.** `structure.levels` is a list of level NAMES and the
corpus holds 12 distinct shapes at depths 2-4 — `(chapter, verse)`, `(adhyaya, pada, sutra)`,
`(mundaka, khanda, mantra)`, `(kanda, prasna, anuvaka)`. `levels` declares the MAXIMUM depth,
not a uniform one: Caraka's Cikitsasthana subdivides adhyayas 1-2 into padas and leaves the
other 28 alone, so a label with fewer components means that branch is not subdivided. A
self-referencing parent_id represents that natively; a fixed text->chapter->verse hierarchy
cannot. (A check that assumed uniform depth accused ~20% of the corpus before the check itself
turned out to be wrong — DECISIONS.md 2026-09-15 D4.)

**Publication is a state on an annotation, and the published surface is a VIEW over it.** The
views and the role grants live in the Alembic migration, not here, because they are privileges
rather than tables. See `tests/test_publication_gate.py`.
"""

from __future__ import annotations

import datetime as _dt

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    text as _sql,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# TWO kinds, not four. M5/B3, 2026-09-16: `phala` and `align` were modelled as annotation
# KINDS, but measuring the corpus shows they are two of NINE tag namespaces --
# rel 6,019 · graha 2,070 · bhava 1,805 · entity 1,318 · mahadasha 690 · rashi 509 ·
# phala 475 · chain 271 · align 210, and every tag carries its namespace as a `prefix:value`
# string. Promoting two of nine to first-class kinds was arbitrary, left the other seven with
# nowhere to record which namespace they came from, and meant nothing ever wrote `phala` or
# `align`. The namespace stays IN the value, where the corpus already puts it, and ordering
# is carried by `annotation.position`.
ANNOTATION_KINDS = ("translation", "tag")
# T6/2026-09-16. FIVE states, not two. The withdrawn two-state mapping would have written
# 55,942 rows asserting a review nobody performed, from `status`, which is an ARRIVAL DATE.
# `approved` is reachable ONLY through the revision surface and ONLY with a named human.
# DECISIONS.md 2026-09-16.
ANNOTATION_STATES = ("draft", "in_review", "needs_revision", "approved", "superseded")
# Which states a consumer may see is a POLICY over states, not a property of them -- the
# published views decide serving; `state` records editorial reality. Keeping those separate is
# what stops "unreviewed" from creating pressure to bulk-promote.
SERVABLE_STATES = ("approved",)
# Who or what produced a revision. The distinction is the whole point of recording provenance:
# "was this reviewed?" is currently answerable only by diffing against HEAD and guessing, and
# that guess produced a false alarm on 2026-09-15.
ANNOTATION_METHODS = ("human", "machine", "matcher")
# T7/D10: the directory middle level, as a FACET TABLE rather than two columns (Rupali's
# override). 52 of 66 texts carry exactly one; a future axis costs a row, not a migration.
FACET_KINDS = ("school", "shakha", "discipline", "recension", "veda")


def _in_list(column: str, values: tuple[str, ...]) -> str:
    """`col IN ('a','b')` built explicitly.

    Was `"kind IN " + str(TUPLE)`, which relies on Python tuple repr happening to be valid
    SQL. It is -- for two or more elements. A ONE-element tuple renders `('draft',)` and the
    trailing comma is a syntax error, so the constraint would have broken the first time a
    list was narrowed to a single value. Explicit over clever.
    """
    return f"{column} IN (" + ", ".join(f"'{v}'" for v in values) + ")"


class Base(DeclarativeBase):
    pass


class Category(Base):
    """A real table so `text.category` can be a foreign key.

    `astroacharya/scripts/validate_corpus.py:41-43` names the defect this closes: category is
    an unvalidated string at ingest, so a typo silently mints a new one and the text becomes
    invisible to every category filter while all counts stay green. Seeded from that file's
    KNOWN_CATEGORIES (21 members; the corpus uses 14 -- the set is a deliberate superset
    covering Youvan's scope).
    """

    __tablename__ = "category"

    name: Mapped[str] = mapped_column(String(48), primary_key=True)
    note: Mapped[str | None] = mapped_column(Text)


class Text_(Base):
    """One classical work. `__tablename__` is `text`; the class is `Text_` to avoid shadowing
    sqlalchemy.Text, which this module also imports."""

    __tablename__ = "text"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)  # the text_id slug
    title_sa: Mapped[str | None] = mapped_column(Text)
    title_en: Mapped[str | None] = mapped_column(Text)
    category: Mapped[str | None] = mapped_column(ForeignKey("category.name", ondelete="RESTRICT"))
    # The whole structure block, unrelationalised on purpose: 18 distinct keys across 49 texts,
    # including known_gaps and count_authority, which no consumer has ever been able to see
    # because _normalize_shloka dropped them. Relationalise later only where a query needs it.
    structure: Mapped[dict | None] = mapped_column(JSONB)
    # sha256 of the source JSON at import, so a re-import is diffable and a stale row detectable.
    source_sha: Mapped[str | None] = mapped_column(String(64))
    # T7/D11: Siddhanta Siromani is one work in four parts sharing a directory -- the only
    # real case in 66 texts. Cross-REPO containment stays in `structure`, because its
    # counterpart lives in another repository and could never be a foreign key.
    part_of: Mapped[str | None] = mapped_column(
        ForeignKey("text.id", ondelete="RESTRICT"), index=True
    )

    facets: Mapped[list[TextFacet]] = relationship(
        back_populates="text", cascade="all, delete-orphan"
    )
    sections: Mapped[list[Section]] = relationship(
        back_populates="text", cascade="all, delete-orphan"
    )


class Section(Base):
    """A node in the ragged tree: chapter, adhyaya, pada, khanda, anuvaka, ...

    `level_name` is stored because it is not decoration -- `adhyaya` vs `kanda` is a real
    distinction that appears in the citation, and the corpus names levels 12 different ways.
    """

    __tablename__ = "section"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    text_id: Mapped[str] = mapped_column(ForeignKey("text.id", ondelete="CASCADE"), index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("section.id", ondelete="CASCADE"), index=True
    )
    depth: Mapped[int] = mapped_column(SmallInteger)
    level_name: Mapped[str] = mapped_column(String(32))
    label: Mapped[str] = mapped_column(String(64))  # literal: "1", "63अ", "Vidyeshvara_Samhita"
    title: Mapped[str | None] = mapped_column(Text)
    # Only 2 chapters carry it, and one is not a translation at all: saravali ch1 holds
    # "Complete Saravali (chapters 1-55, not yet split)" -- a STRUCTURAL CAVEAT. Dropping
    # the column would drop the caveat, which is the kind of loss `structure` already
    # suffered under _normalize_shloka.
    title_en: Mapped[str | None] = mapped_column(Text)
    position: Mapped[int] = mapped_column(Integer)  # sibling order, from source array order

    text: Mapped[Text_] = relationship(back_populates="sections")
    parent: Mapped[Section | None] = relationship(remote_side=[id], back_populates="children")
    children: Mapped[list[Section]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
    verses: Mapped[list[Verse]] = relationship(
        back_populates="section", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # A label is unique among its siblings, not globally: chapter 1 exists in every text.
        # parent_id is NULLable and NULL never equals NULL in SQL, so top-level sections are
        # covered by the second constraint instead.
        UniqueConstraint("text_id", "parent_id", "label", name="uq_section_sibling_label"),
        # T1/G58, 2026-09-16. The constraint above does NOT cover top-level sections: NULL is
        # never equal to NULL in SQL, so two chapters both labelled "1" in one text committed
        # silently (reproduced before this fix). The comment that used to sit here claimed they
        # were "covered by the second constraint instead" and named a NON-UNIQUE index.
        Index(
            "uq_section_root_label",
            "text_id",
            "label",
            unique=True,
            postgresql_where=_sql("parent_id IS NULL"),
        ),
        Index("ix_section_text_depth", "text_id", "depth"),
        CheckConstraint("depth >= 1", name="ck_section_depth_positive"),
    )


class TextFacet(Base):
    """One classification axis for one text -- `(bphs, school, Parashari)`.

    A table rather than columns on `text` because the axes are open-ended: five kinds today
    (school 17 texts, shakha 20, discipline 8, veda 5, recension 2), and 14 texts carry none
    -- four of those being the Siromani parts, which share a directory and are handled by
    `text.part_of` instead.
    """

    __tablename__ = "text_facet"

    text_id: Mapped[str] = mapped_column(
        ForeignKey("text.id", ondelete="CASCADE"), primary_key=True
    )
    kind: Mapped[str] = mapped_column(String(16), primary_key=True)
    value: Mapped[str] = mapped_column(String(64), primary_key=True)

    text: Mapped[Text_] = relationship(back_populates="facets")

    __table_args__ = (
        CheckConstraint(_in_list("kind", FACET_KINDS), name="ck_facet_kind"),
        Index("ix_facet_kind_value", "kind", "value"),
    )


class Verse(Base):
    """A shloka. The unit a citation points at."""

    __tablename__ = "verse"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    section_id: Mapped[int] = mapped_column(
        ForeignKey("section.id", ondelete="CASCADE"), index=True
    )
    # THE LITERAL LABEL. Never parsed for ordering. 11 shapes occur, including half-shlokas
    # ("27 1/2"), Devanagari suffixes ("12अ"), hyphen sub-numbers ("1.12-3") and digit-strings
    # that look like ints but are not ("140" in nirnayasindhu).
    number_label: Mapped[str] = mapped_column(String(64))
    # Whether the source JSON held `number` as a STRING rather than an int. Not cosmetic and
    # not derivable: 32 labels are pure ASCII digits that were typed `str` (nirnayasindhu), so
    # once the label is TEXT the two are indistinguishable -- and `export --mode fidelity`
    # cannot reproduce the committed corpus without it. 4 texts (bphs, jataka_parijata,
    # mayamata, yajusha_jyotisham) MIX both types, so it cannot live on `text` either.
    # Chapter labels need no equivalent: 952 int, 3 str, and all 3 are Devanagari-suffixed
    # (`63अ`), so their type IS recoverable from the string.
    number_is_str: Mapped[bool] = mapped_column(Boolean, server_default=_sql("false"))
    # ORDERING, assigned from the source array order at import. Array order is authoritative --
    # it is what the edition emitted -- and it disagrees with numeric label order in 17
    # chapters, which is a recorded reconciliation finding, not a bug to "fix" at read time.
    position: Mapped[int] = mapped_column(Integer)
    devanagari: Mapped[str] = mapped_column(Text)
    ref: Mapped[str | None] = mapped_column(Text)  # rendered citation; present on 71,929 of 97,794
    # 709 verses carry it, all in saravali. G12's lesson is that metre notes are what identify
    # a unit when its number lies, so dropping this would discard the thing that resolves G12.
    meter: Mapped[str | None] = mapped_column(String(64))
    # T5/2026-09-16. THE ARRIVAL FIELD, and deliberately NOT the editorial state.
    # It records WHEN a translation arrived, never whether anyone checked it: measured,
    # ('untranslated', has_english=True, has_hindi=True) = 69,813 verses. It was omitted from
    # the first schema as "derivable from annotation.state" -- true under the withdrawn
    # two-state mapping, false the moment that mapping went, and green either way because
    # nothing tested the justification. Without it `export --fidelity` cannot round-trip.
    status: Mapped[str | None] = mapped_column(String(16))

    section: Mapped[Section] = relationship(back_populates="verses")
    annotations: Mapped[list[Annotation]] = relationship(
        back_populates="verse", cascade="all, delete-orphan"
    )

    __table_args__ = (
        # G8, turned from silent loss into a failed import. seed_texts.py dedupes on
        # (chapter, shloka) with later-file-wins and logs a warning; 70 verses are lost that
        # way today across jataka_parijata (55), laghu_jatakam (14), minaraja (1). Each is data
        # to fix, never a constraint to relax.
        UniqueConstraint("section_id", "number_label", name="uq_verse_label_in_section"),
        UniqueConstraint("section_id", "position", name="uq_verse_position_in_section"),
    )


class Annotation(Base):
    """Current state of one annotation on one verse: a translation, a tag, a phala, an align.

    A verse can hold BOTH an approved and a draft value for the same (kind, lang)
    simultaneously -- 2,369 draft-bearing verses also carry populated english/hindi -- so the
    uniqueness constraint is PARTIAL, over APPROVED rows only. The predicate tracks the state
    name: pointing it at a state no row can reach makes it match nothing and constrain nothing.
    """

    __tablename__ = "annotation"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    verse_id: Mapped[int] = mapped_column(ForeignKey("verse.id", ondelete="CASCADE"), index=True)
    kind: Mapped[str] = mapped_column(String(16))
    lang: Mapped[str | None] = mapped_column(String(8))  # NULL for tag/phala/align
    value: Mapped[str] = mapped_column(Text)
    # WHICH JSON FIELD this came from -- `english`, `english_draft`, `tags`, `tags_draft`.
    # A FACT about import provenance, not a claim about authorship: a value sitting in
    # `english` may be curated or a promoted machine draft, and the corpus does not record
    # which. Needed because UC1 lands BOTH the served value and its draft as `state='draft'`
    # with identical (kind, lang), so nothing else tells them apart -- and without it
    # `export --mode fidelity` cannot put them back in the right keys.
    source_field: Mapped[str | None] = mapped_column(String(16))
    # T9: tags arrive as an ARRAY and an array has an order. Without this the importer
    # cannot round-trip `tags`, because rows come back in whatever order the planner picks.
    # NULL for translations, where ordering is meaningless.
    position: Mapped[int | None] = mapped_column(Integer)
    state: Mapped[str] = mapped_column(String(16), server_default=_sql("'draft'"))
    current_revision_id: Mapped[int | None] = mapped_column(BigInteger)

    verse: Mapped[Verse] = relationship(back_populates="annotations")
    revisions: Mapped[list[AnnotationRevision]] = relationship(
        back_populates="annotation", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(_in_list("kind", ANNOTATION_KINDS), name="ck_annotation_kind"),
        CheckConstraint(_in_list("state", ANNOTATION_STATES), name="ck_annotation_state"),
        # PARTIAL: one approved value per (verse, kind, lang); drafts are unconstrained so a
        # pending edit can sit beside the live one. Without the partial clause, importing the
        # corpus as it stands would have to silently drop one side of 2,369 verses.
        # T7: the published view joins annotation on (verse_id, state); the partial unique
        # index below covers only approved rows, so the draft side would scan without this.
        Index("ix_annotation_verse_state", "verse_id", "state"),
        Index(
            "uq_annotation_approved",
            "verse_id",
            "kind",
            "lang",
            unique=True,
            postgresql_where=_sql("state = 'approved'"),
        ),
    )


class AnnotationRevision(Base):
    """Append-only history. NEVER updated, never deleted.

    This is the capability the corpus has not had: "was this reviewed, by whom, and what did it
    say before?" On 2026-09-15 that question was answerable only by diffing the working tree
    against HEAD and inferring -- and the inference was wrong, reading a deliberate curated
    promotion as an unreviewed machine one. Recording author and method makes it a fact rather
    than a reconstruction.
    """

    __tablename__ = "annotation_revision"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # T3/G60, 2026-09-16. RESTRICT, not CASCADE. This class is documented as "NEVER updated,
    # never deleted" and was CASCADE at every hop from `text`, so deleting one text erased the
    # provenance the whole store exists to add. The docstring was the only thing enforcing it.
    # The migration adds the BEFORE UPDATE OR DELETE trigger that makes it true of the DATA.
    # NOT index=True: SQLAlchemy would auto-name it ix_annotation_revision_annotation_id
    # while the migration creates ix_revision_annotation_id, and the two definitions would
    # describe different schemas. Caught by tests/test_schema_drift.py on its first run.
    annotation_id: Mapped[int] = mapped_column(
        ForeignKey("annotation.id", ondelete="RESTRICT")
    )
    value: Mapped[str] = mapped_column(Text)
    state: Mapped[str] = mapped_column(String(16))
    author: Mapped[str | None] = mapped_column(String(128))
    method: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[_dt.datetime] = mapped_column(
        DateTime(timezone=True), server_default=_sql("now()")
    )
    supersedes_id: Mapped[int | None] = mapped_column(
        ForeignKey("annotation_revision.id", ondelete="SET NULL")
    )
    note: Mapped[str | None] = mapped_column(Text)

    annotation: Mapped[Annotation] = relationship(back_populates="revisions")

    __table_args__ = (
        CheckConstraint(_in_list("method", ANNOTATION_METHODS), name="ck_revision_method"),
        CheckConstraint(_in_list("state", ANNOTATION_STATES), name="ck_revision_state"),
        Index("ix_revision_annotation_id", "annotation_id"),
        Index("ix_revision_annotation_created", "annotation_id", "created_at"),
    )
