"""`models.py` and `0001` are two hand-maintained schema definitions. Assert they agree.

WHY THIS EXISTS. The corpus has two independent descriptions of the same tables: the
SQLAlchemy models the package reads through, and the Alembic migration the database is
actually built from. Nothing compared them, so a column could have a home in `models.py`
that the database did not have -- and `tests/test_key_census.py` reads the MODELS, so it
would have called that key modelled while every query against it failed.

This is the mechanical half of the declared propagate edge
`sanskrit_texts/models.py -> migrations/versions/0001_corpus_schema_and_gate.py`. The edge
says the two must move together; this test is what makes that enforceable rather than
aspirational (rule:adversarial-review-reads-the-ledger: a declaration nothing tests is the
same failure in a new place).
"""

from __future__ import annotations

import pytest
from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext

from sanskrit_texts.models import Base

# The migration creates things SQLAlchemy metadata does not describe and cannot reflect into
# a model: two VIEWS (the published surface), the append-only TRIGGER and its function, and
# the role grants. Alembic sees the views as unknown tables, so they are named here rather
# than silently swallowed by a broad filter.
NOT_IN_METADATA = {"alembic_version", "published_text", "published_verse"}


def _include(object_, name, type_, reflected, compare_to):
    """Alembic's include_object signature -- five positional args, not three.

    Getting this wrong raises TypeError rather than quietly returning an empty diff, which
    is the failure mode you want from a filter on a check whose whole job is noticing.
    """
    if type_ == "table":
        return name not in NOT_IN_METADATA
    return True


def test_models_and_migration_describe_the_same_schema(owner_engine):
    """Run against the REAL migrated database, not a metadata.create_all() of the models.

    Comparing the models to themselves would pass unconditionally, which is the failure
    rule:discernment-checks §1 is about.
    """
    with owner_engine.connect() as conn:
        ctx = MigrationContext.configure(conn, opts={"include_object": _include,
                                                     "compare_type": False})
        diff = compare_metadata(ctx, Base.metadata)
    # compare_metadata still surfaces the views as remove_table entries on some versions;
    # drop those explicitly so a REAL removed table is never hidden by a broad filter.
    real = [
        d for d in diff
        if not (isinstance(d, tuple) and len(d) == 2 and d[0] == "remove_table"
                and getattr(d[1], "name", None) in NOT_IN_METADATA)
    ]
    assert not real, (
        "models.py and 0001 disagree about the schema:\n  "
        + "\n  ".join(repr(d) for d in real)
        + "\nAmend BOTH, or the census will call a key modelled that the database lacks."
    )


def test_the_drift_check_can_actually_fail(owner_engine):
    """rule:discernment-checks §1 -- ship the input that makes the check fail.

    Adds a column to the in-memory metadata only (never to the database) and asserts the
    comparison notices. Without this, a `compare_metadata` that silently returned [] -- a
    wrong `include_object`, a bad connection -- would report agreement forever.
    """
    import sqlalchemy as sa

    verse = Base.metadata.tables["verse"]
    probe = sa.Column("zz_drift_probe", sa.String(8))
    verse.append_column(probe)
    try:
        with owner_engine.connect() as conn:
            ctx = MigrationContext.configure(conn, opts={"include_object": _include,
                                                         "compare_type": False})
            diff = compare_metadata(ctx, Base.metadata)
        found = any("zz_drift_probe" in repr(d) for d in diff)
        assert found, "the drift check did not notice a column present in models and absent in the DB"
    finally:
        verse._columns.remove(probe)
