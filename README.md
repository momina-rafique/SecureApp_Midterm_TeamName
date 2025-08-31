# QuickQuickNotes API

[![CI](https://github.com/yourusername/fastapi-notes-api/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/fastapi-notes-api/actions)

A lightweight yet practical QuickNotes API built with **FastAPI**, designed to be simple enough to follow but solid enough to demo in a programming club. It has:

- User accounts with signup/login (JWT auth)
- Ownership on notes (each user manages their own)
- Tags, search, pagination, archive support
- Config via `.env` (SQLite default, Postgres-ready)
- Clean codebase (SQLAlchemy 2.0 + Pydantic v2)
- Tests (pytest) covering auth + CRUD
- Docker/Render/Railway deploy ready

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs
```

## Auth flow
1. `POST /auth/signup` (email, password)
2. `POST /auth/login` → returns Bearer token
3. Use `Authorization: Bearer <token>` for `/api/notes/*`

## Notes features
- Create/read/update/delete notes
- Assign tags by names; auto-create
- Search `q` on title/content, filter by `tag`, `archived`
- Pagination: `limit` (1–100), `offset`
- Sorted by `updated_at` desc

## Deployment

### Render
- Push repo to GitHub → create new **Web Service** on Render
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Add env vars (`SECRET_KEY`, etc). If you add Postgres, Render sets `DATABASE_URL` automatically.

### Railway
- New project → Deploy from GitHub
- Add Postgres plugin (Railway sets `DATABASE_URL`)
- Start command already in `railway.json`

### Docker (local)
```bash
docker build -t notes-api .
docker run -p 8000:8000 -e SECRET_KEY=dev notes-api
# http://127.0.0.1:8000/docs
```
Or with Postgres:
```bash
docker compose up --build
```

## Tests
```bash
pytest -q
```

---

## Roadmap / Ideas
- Rate limiting on login
- Refresh tokens
- User profile endpoints
- UI client (React/Vue) consuming the API

---

💡 _This repo is intentionally kept straightforward. The goal is to demonstrate good practices (auth, tests, CI, deployment) without overengineering._

Last updated: 2025-08-31
