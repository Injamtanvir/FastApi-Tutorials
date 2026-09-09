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
