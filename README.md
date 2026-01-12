# FastAPI Project

A minimal FastAPI application with versioned API, JWT auth, PostgreSQL (runtime) with SQLite for tests, and tests.

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
├── README.md                    # Documentation: quick start, API, structure
├── requirements.txt             # Python deps (FastAPI, SQLAlchemy, passlib, ...)
├── alembic/
│   └── README.md                # Notes for configuring migrations later
├── app/                         # FastAPI application source
│   ├── main.py                  # App factory: adds middleware, includes v1 router,
│   │                             # creates tables, seeds default products if empty.
│   ├── api/
│   │   └── v1/
│   │       ├── router.py        # Aggregates endpoints under /api/v1.
│   │       └── endpoints/
│   │           ├── auth.py      # POST /auth/login issues JWT for email+password.
│   │           ├── users.py     # POST /users registers; GET /users/me returns
│   │                             # current profile.
│   │           ├── items.py     # Auth-required item create/list examples.
│   │           ├── products.py  # List insurance products; basis to purchase.
│   │           ├── policies.py  # Create/view policies linked to users/products.
│   │           ├── claims.py    # File claims and fetch status; supports
│   │                             # real-time checks.
│   │           └── advisory.py  # Advisory: tailored tips from profile & claims.
│   ├── core/
│   │   ├── config.py            # Pydantic settings from env (.env), e.g., DB URL.
│   │   └── security.py          # Bcrypt hashing, JWT create/decode, OAuth2.
│   │                             # Provides get_current_user for protected routes.
│   ├── db/
│   │   ├── base.py              # SQLAlchemy Base for ORM models.
│   │   └── session.py           # Engine & SessionLocal; switches to test.db under
│   │                             # pytest for clean runs.
│   ├── dependencies/
│   │   └── get_db.py            # Yields a per-request DB session; closes on finish.
│   ├── middleware/
│   │   └── logging.py           # Adds X-Process-Time-ms header for basic tracing.
│   ├── models/
│   │   ├── user.py              # User: email, hashed_password, is_active, items.
│   │   ├── item.py              # Item: title, description, owner relationship.
│   │   ├── product.py           # Product: name, description; seeds defaults.
│   │   ├── policy.py            # Policy: links user↔product; stores status & dates.
│   │   └── claim.py             # Claim: references policy; tracks state & details.
│   ├── schemas/
│   │   ├── user.py              # Pydantic: UserCreate/UserRead models.
│   │   ├── item.py              # Pydantic: ItemCreate/ItemRead models.
│   │   ├── product.py           # Pydantic: ProductRead (+ inputs when purchasing).
│   │   ├── policy.py            # Pydantic: PolicyCreate/PolicyRead.
│   │   └── claim.py             # Pydantic: ClaimCreate/ClaimRead.
│   └── services/
│       ├── user_service.py      # User persistence & auth helpers (hash/verify).
│       ├── item_service.py      # Item CRUD with owner checks.
│       ├── product_service.py   # Product queries; seed_default_products helper.
│       ├── policy_service.py    # Issue/cancel policy; associate to user & product.
│       ├── claim_service.py     # Open/update claim; status progression utilities.
│       └── advisory_service.py  # Compute advisory output from user, policy, claims.
└── tests/
  ├── test_auth.py             # Verifies login rejects bad creds; token issuance.
  └── test_users.py            # Register user; login; fetch /users/me with token.
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
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
```

PostgreSQL setup (local example):

```bash
# Ensure PostgreSQL is installed and running
# Create a database for the app
psql -U postgres -h localhost -c "CREATE DATABASE fastapi_db;"
```

Notes:

- The app uses PostgreSQL by default via `DATABASE_URL`.
- Tests run against an isolated SQLite `test.db` automatically under pytest for determinism.

## Migrations (Alembic)

Alembic folder is scaffolded. Initialize if you plan migrations:

```bash
alembic init alembic
```

Then configure `alembic.ini` and `env.py` to point to your `DATABASE_URL` (e.g., `postgresql://...`).

## Deprecation Hygiene

- Startup events were replaced with immediate table creation in the app factory
  to avoid deprecated `on_event` usage.
- Security tokens use timezone-aware datetimes (`datetime.now(datetime.UTC)`)
  instead of `datetime.utcnow()`.

## Credits & Contact

- Project by Isaiah Kimoban.
- Email: <isaiahkimoban87@gmail.com>
- LinkedIn: <https://www.linkedin.com/in/kimoban/>
