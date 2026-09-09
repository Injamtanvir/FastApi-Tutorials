# Expense Tracker API

A simple CRUD API for tracking personal expenses, built with **FastAPI** and
**PostgreSQL** (via SQLAlchemy). Originally started as a JSON-file prototype
and upgraded here to a real database with environment-based configuration,
ready to deploy on Render.

## Project structure

```
expense_tracker/
├── main.py          # FastAPI app + routes
├── database.py       # DB engine/session, reads DATABASE_URL from .env
├── models.py          # SQLAlchemy ORM table definition
├── schemas.py          # Pydantic request/response models
├── requirements.txt
├── .env.example         # template — copy to .env locally
├── .gitignore
└── Procfile               # tells Render how to start the app
```

## Why it's structured this way

- **`models.py` vs `schemas.py`** — `models.py` describes the actual
  database table (SQLAlchemy). `schemas.py` describes what the API
  accepts and returns (Pydantic). Keeping them separate means you can
  change your API's public shape without touching your table, and vice
  versa — a pattern you'll see in most real FastAPI codebases.
- **`.env` for secrets** — the database password/URL is never hardcoded.
  `database.py` loads it via `python-dotenv` + `os.getenv(...)`, with a
  SQLite fallback so the app still runs even if you forget to set `.env`.
- **`get_db()` dependency** — opens one DB session per request and always
  closes it, even on errors. This is FastAPI's standard pattern for DB
  access.

## Running it locally

1. Install PostgreSQL locally (or use any hosted Postgres you have) and
   create a database:
   ```
   createdb expense_tracker
   ```
2. Copy the env template and fill in your real password:
   ```
   cp .env.example .env
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the server:
   ```
   uvicorn main:app --reload
   ```
5. Open the interactive docs at `http://127.0.0.1:8000/docs` and try the
   routes directly from the browser.

## Deploying on Render (free tier)

1. **Push this folder to a GitHub repo.** (`.env` is git-ignored on
   purpose — you'll set the real value in Render's dashboard instead.)
2. **Create a Postgres database on Render:**
   - Render dashboard → New → PostgreSQL → pick a name/region → Create.
   - Once it's up, copy the **Internal Database URL** it gives you.
3. **Create a Web Service on Render:**
   - New → Web Service → connect your GitHub repo.
   - Runtime: Python 3.
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     (Render also auto-detects the `Procfile`, so this is a backup.)
4. **Set the environment variable:**
   - In the Web Service → Environment tab, add:
     `DATABASE_URL` = the Internal Database URL from step 2
   - Important: Render's Postgres URL starts with `postgresql://` — for
     this project's SQLAlchemy driver, change that prefix to
     `postgresql+psycopg://` so it reads
     `postgresql+psycopg://user:pass@host/dbname`.
5. **Deploy.** Render builds and starts the service; your API will be
   live at `https://<your-service-name>.onrender.com`, with interactive
   docs at `/docs`.

## API routes

| Method | Route              | Description                          |
|--------|---------------------|---------------------------------------|
| GET    | `/`                  | Health check                          |
| GET    | `/view`              | List all expenses                      |
| GET    | `/view/{expense_id}` | Get one expense by ID                   |
| GET    | `/sort`              | List sorted by `sorted_by` + `order`     |
| POST   | `/create`            | Create a new expense                     |
| PUT    | `/edit/{expense_id}` | Partially update an expense               |
| DELETE | `/delete/{expense_id}` | Delete an expense                        |

## Talking about this project in an interview

A few things worth mentioning:
- Why you separated ORM models from Pydantic schemas.
- Why secrets live in environment variables, not source code.
- What `exclude_unset=True` does and why partial updates need it.
- The tradeoff of using `Base.metadata.create_all()` (simple, no
  migration history) vs. Alembic (tracked, reversible schema changes) —
  and that you'd reach for Alembic next as the project grows.
