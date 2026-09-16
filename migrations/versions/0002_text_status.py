"""text.status -- the text-level summary 28 files carry

Revision ID: 0002_text_status
Revises: 0001_corpus_schema_and_gate
Create Date: 2026-09-16

0001 omitted this key as "derivable from its verses". It was not reproducible by the exporter
-- 38 of 66 files have no such key, so derivation alone cannot say WHICH texts to emit it for
-- and the round trip failed on the 28 that do. Nullable: NULL is "the file has no key".

0001 is pushed, so this is a new revision rather than an amendment.
"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision = "0002_text_status"
down_revision = "0001_corpus_schema_and_gate"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("text", sa.Column("status", sa.String(16), nullable=True))


def downgrade() -> None:
    op.drop_column("text", "status")
