# Backend API

This project is a **FastAPI backend** that manages **users** and **gift cards** with support for file uploads (e.g., PDF or images) and spending tracking.

## Features

- User management (create, list, delete).
- Gift card management (create, list, delete, spend tracking).
- Upload/download a file (PDF or image) associated with a gift card (one-to-one relation).
- Pagination, sorting, and filtering.
- Async SQLAlchemy with PostgreSQL.

## Project Structure

```
backend/
├── routers/        # FastAPI routers (users, giftcards)
├── logic/          # Business logic
├── model/          # ORM models and Pydantic converters
├── utility/        # Database session helpers
├── tests/          # Pytest-based test suite
└── main.py         # FastAPI entrypoint
```

## Requirements

- Python >= 3.13
- PostgreSQL
- Dependencies (see `pyproject.toml`):
  - FastAPI
  - SQLAlchemy
  - asyncpg
  - Pydantic

## Running the App

1. Install dependencies:

```bash
uv pip install -r pyproject.toml
```

or with **uv** (recommended):

```bash
uv sync
```

2. Run database migrations (if you use Alembic):

```bash
alembic upgrade head
```

3. Start the app:

```bash
uvicorn backend.main:app --reload
```

4. Open docs in the browser:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Endpoints

### Users

- `GET /users/` → List users (with pagination, sorting).
- `GET /users/{user_id}` → Get a single user (optionally include gift cards).
- `POST /users/` → Create a new user.
- `DELETE /users/{user_id}` → Delete a user.

### Gift Cards

- `GET /giftcards/` → List gift cards with filters and sorting.
- `GET /giftcards/{giftcard_id}` → Get a single gift card.
- `POST /giftcards/` → Create a gift card.
- `DELETE /giftcards/{giftcard_id}` → Delete a gift card.
- `PATCH /giftcards/{giftcard_id}/spend` → Increment spent amount.
- `POST /giftcards/{giftcard_id}/upload` → Upload a file (PDF or image).
- `GET /giftcards/{giftcard_id}/download` → Download the attached file.

## Database Schema

- **User**: has many gift cards.
- **GiftCard**: belongs to one user, has an optional attached file.
- **File**: one-to-one with a gift card.

```sql
CREATE TABLE "user" (
    id UUID PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE "file" (
    id UUID PRIMARY KEY,
    giftcard_id UUID UNIQUE REFERENCES "giftcard" (id) ON DELETE CASCADE,
    filename VARCHAR NOT NULL,
    content_type VARCHAR NOT NULL,
    data BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);

CREATE TABLE giftcard (
    id UUID PRIMARY KEY,
    supplier VARCHAR NOT NULL,
    amount INTEGER NOT NULL,
    spent_amount INTEGER NOT NULL,
    user_id UUID REFERENCES "user" (id) ON DELETE SET NULL,
    file_id UUID REFERENCES "file" (id) ON DELETE SET NULL,
    expiration_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL
);
```

## Testing

Run the tests with:

```bash
pytest
```

