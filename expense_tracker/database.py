# database.py
# Handles the database connection setup.
# The actual connection string lives in the .env file (never in code, never in git)
# and is loaded here using python-dotenv + os.

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Reads the .env file in the project root and loads its key=value pairs
# into the process environment (os.environ).
load_dotenv()

# os.getenv() reads the DATABASE_URL variable that .env just loaded.
# The second argument is a fallback used only if DATABASE_URL is missing,
# so the app still runs locally on SQLite even if you forget to set .env.
SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./expenses.db"
)

# Hosting providers (Render, Railway, Heroku, etc.) commonly hand out
# Postgres URLs starting with "postgres://" or plain "postgresql://".
# SQLAlchemy defaults *either* of those to the psycopg2 driver, which we
# never install (we use psycopg v3 instead). Rather than relying on every
# environment variable being typed exactly right, we normalize the scheme
# here in code so the app always ends up using the psycopg v3 driver no
# matter what format the URL arrives in.
if SQLALCHEMY_DATABASE_URL.startswith("postgres://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

# connect_args is only needed for SQLite (it disallows multi-thread access
# by default). Postgres doesn't need this, so we add it conditionally.
connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    FastAPI dependency: opens a DB session for a single request,
    hands it to the route function, and always closes it afterwards
    (even if the route raises an error).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
