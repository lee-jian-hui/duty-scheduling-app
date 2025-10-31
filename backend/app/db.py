from __future__ import annotations

import os
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


class Base(DeclarativeBase):
    pass


def _database_url() -> str:
    # Default to a SQLite file inside backend/app
    return os.getenv("DATABASE_URL", "sqlite:///backend/app/app.db")


# SQLite needs check_same_thread=False for use across threads (e.g., FastAPI)
_engine = create_engine(_database_url(), connect_args={"check_same_thread": False} if _database_url().startswith("sqlite") else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


__all__ = ["Base", "SessionLocal", "get_db"]

