from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _database_url() -> str:
    # Prefer explicit environment variable
    env = os.getenv("DATABASE_URL")
    if env:
        return env
    # Default to a SQLite file next to this module (backend/app/app.db)
    here = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(here, "app.db")
    return f"sqlite:///{db_path}"


# SQLite needs check_same_thread=False for use across threads (e.g., FastAPI)
_URL = _database_url()

# For SQLite, enable cross-thread access and set a connection timeout so the driver
# waits for concurrent locks instead of failing immediately.
_connect_args = {"check_same_thread": False, "timeout": 30} if _URL.startswith("sqlite") else {}
_engine = create_engine(_URL, connect_args=_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)

# Apply SQLite pragmas on each new connection to improve concurrency.
if _URL.startswith("sqlite"):
    @event.listens_for(_engine, "connect")
    def _set_sqlite_pragma(dbapi_connection, connection_record):  # type: ignore[no-redef]
        cursor = dbapi_connection.cursor()
        # WAL allows readers and writers to not block each other.
        cursor.execute("PRAGMA journal_mode=WAL;")
        # Busy timeout in milliseconds; complements the driver-level timeout above.
        cursor.execute("PRAGMA busy_timeout=5000;")
        # Reasonable durability with better performance for web workloads.
        cursor.execute("PRAGMA synchronous=NORMAL;")
        cursor.close()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "SessionLocal", "get_db"]
