from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
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
_engine = create_engine(_URL, connect_args={"check_same_thread": False} if _URL.startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "SessionLocal", "get_db"]
