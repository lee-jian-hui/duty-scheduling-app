##  Development environment and versions
- WSL Ubuntu 22.04
- python 3.10.12
- node v20.19.5
- npm 10.8.2

## PRE-REQUISITES
- node.js
- npm
- python pip
- install uv `pip install uv`

## NOTES:
- backend runs on `:8000`
- frontend runs on `:5173` and `:4173` respectively
- Database sqllite will be in `backend/app`
- The database is already seeded with initial dummy data


#### Setup SQLLITE DB (MUST DO THIS FIRST)
```
cd backend/app
alembic history
alembic upgrade head
```

### Start Backend
```
cd backend
uv sync
#   Backend will run on http://localhost:8000
uv run python -m app.main
```

### Start Frontend
build prod and run preview
```
cd frontend
npm install
npm run build
#  Frontend will run on http://localhost:4173
npm run preview
```
  Development mode:
```
cd frontend
npm install
npm run dev
Frontend will run on http://localhost:5173
```


### Database & Alembic (SQLite)

This repo includes a minimal SQLAlchemy + Alembic setup using SQLite.

- Connection URL: `DATABASE_URL` (defaults to `sqlite:///backend/app/app.db`)
- SQLAlchemy base/session: `app/db.py`
- ORM models for migrations: `app/core/db_models/*`
- Alembic setup: `alembic.ini`, `alembic/`, with an initial migration

Setup steps:

1) Install dependencies in the backend venv

```
pip install sqlalchemy alembic
```

2) Run migrations from the repo root

```
alembic upgrade head
```

3) Optional: customize the `DATABASE_URL` env var and re-run migrations.

Notes:

- The app still uses in-memory repositories by default. You can add DB-backed repositories later and inject them via `app/deps.py`.

