from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool


# Ensure the Python path includes the directory that contains the
# `app` package (the backend/ folder). This makes `import app` work
# regardless of the current working directory when running Alembic.
HERE = Path(__file__).resolve()
BACKEND_DIR = HERE.parents[3]  # .../backend
if str(BACKEND_DIR) not in sys.path:
    sys.path.append(str(BACKEND_DIR))

# Import SQLAlchemy Base and ensure models are imported so metadata is populated
from app.db import Base  # type: ignore  # noqa: E402
from app.core import db_models as _models  # type: ignore  # noqa: E402,F401


# Alembic Config object, provides access to the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for 'autogenerate'
target_metadata = Base.metadata


def _database_url() -> str:
    # Prefer DATABASE_URL if provided
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url
    # Default to SQLite DB located at backend/app/app.db
    app_dir = HERE.parents[2]  # .../backend/app
    db_path = app_dir / "app.db"
    return f"sqlite:///{db_path}"


def run_migrations_offline() -> None:
    url = _database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Ensure the URL is set even if the ini has a placeholder
    config.set_main_option("sqlalchemy.url", _database_url())

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

