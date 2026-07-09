# URL Shortener

A simple URL shortening service built with FastAPI and SQLAlchemy.

## Features

- Create a short code for any URL
- Redirect short codes to the original URL
- Tracks click counts

## Requirements

- Python 3.10+
- A SQL database supported by SQLAlchemy (configured via `DATABASE_URL`)
- See `requirements.txt` for Python dependencies

## Quick Setup

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv venv
.\n+venv\Scripts\Activate.ps1
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure the database connection by setting `DATABASE_URL` in `app/config.py` or your environment.

4. Run migrations (Alembic):

```bash
alembic upgrade head
```

5. Start the app (development):

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## API Endpoints

- `POST /api/shorten` — Create a shortened URL
  - Body (JSON): `{ "url": "https://example.com" }`
  - Response: `short_code`, `original_url`, `clicks`, `created_at`

- `GET /api/{short_code}` — Redirect to the original URL (returns a 307 redirect)

Swagger UI is available at `/docs` and OpenAPI at `/openapi.json`.

Note: this project mounts the router with the `/api` prefix, so short codes are reachable at `/api/{short_code}` (for example `http://127.0.0.1:8000/api/5Jr9Iv`).

## Common issues

- 404 when accessing a short code: ensure you are requesting the endpoint with the `/api` prefix (for example `GET /api/5Jr9Iv`).
- Swagger UI sometimes URL-encodes surrounding quotes when you paste the short code into the Try-it-out box (e.g. `%225Jr9Iv%22`). The application now strips surrounding single/double quotes from the path parameter before lookup to be tolerant of that input.

## Development notes

- Database models are defined in `app/models.py` and migrations in `alembic/`.
- Routes are in `app/routes/url.py`.
- To serve short codes from the root (without `/api`), remove the `prefix="/api"` argument in `app/main.py` where the router is included.

## Example curl commands

Create a short URL:

```bash
curl -X POST "http://127.0.0.1:8000/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}'
```

Follow a short URL (will return a 307 redirect):

```bash
curl -i http://127.0.0.1:8000/api/5Jr9Iv
```

## License

This project has no license specified.
