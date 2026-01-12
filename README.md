# FastAPI Project

A minimal FastAPI application with versioned API, JWT auth, SQLite DB, and tests.

## Quick Start

1. Create a virtual environment (optional but recommended):

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

1. Install dependencies:

```bash
pip install -r requirements.txt
```

1. Run the app:

```bash
uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>

## Project Structure

```text
FastAPI Project/
├── README.md
├── requirements.txt
├── alembic/
│   └── README.md
├── app/
│   ├── main.py
│   ├── api/
│   │   └── v1/
│   │       ├── router.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           ├── items.py
│   │           └── users.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── dependencies/
│   │   └── get_db.py
│   ├── middleware/
│   │   └── logging.py
│   ├── models/
│   │   ├── item.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── item.py
│   │   └── user.py
│   └── services/
│       ├── item_service.py
│       └── user_service.py
└── tests/
    ├── test_auth.py
    └── test_users.py
```

## API Overview

- POST `/api/v1/users/` – Register a user
- POST `/api/v1/auth/login` – Login, returns JWT
- GET `/api/v1/users/me` – Get current user
  - Requires header: `Authorization: Bearer <token>`
- POST `/api/v1/items/` – Create item (auth required)
- GET `/api/v1/items/` – List items (auth required)

## Testing

```bash
python -m pytest -q
```

Notes:
- Tables are auto-created at app startup.
- During tests, the schema is reset automatically to ensure clean runs.
- Requirements include `email-validator` and pinned `bcrypt==4.0.1` for passlib compatibility.

## Environment

Configuration via `.env`:

```env
SECRET_KEY=devsecret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./app.db
```

## Migrations (Alembic)

Alembic folder is scaffolded. Initialize if you plan migrations:

```bash
alembic init alembic
```

Then configure `alembic.ini` and `env.py` to point to your `DATABASE_URL`.

## Deprecation Hygiene

- Startup events were replaced with immediate table creation in the app factory
  to avoid deprecated `on_event` usage.
- Security tokens use timezone-aware datetimes (`datetime.now(datetime.UTC)`)
  instead of `datetime.utcnow()`.
