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


