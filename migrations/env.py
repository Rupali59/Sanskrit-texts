"""Alembic environment.

THE DSN COMES FROM THE ENVIRONMENT, NOT alembic.ini. The generated ini ships a
`sqlalchemy.url` placeholder; leaving a real one there would put the owner password in a
tracked file. `CORPUS_OWNER_DSN` is the same variable `tests/conftest.py` reads, so the
migration and the tests cannot drift onto different databases.
"""

from __future__ import annotations

import os
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from sanskrit_texts.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

DSN = os.environ.get(
    "CORPUS_OWNER_DSN",
    "postgresql+psycopg://corpus_owner:corpus_local_dev@127.0.0.1:5433/sanskrit_texts",
)
config.set_main_option("sqlalchemy.url", DSN)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=DSN,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
