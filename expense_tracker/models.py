# models.py
# Defines the actual database table using SQLAlchemy's ORM.
# This replaces the old expenses.json file — rows in Postgres instead of
# lines in a JSON file.

from sqlalchemy import Column, String, Float
from database import Base


class Expense(Base):
    __tablename__ = "expenses"

    # Using the human-given ID (e.g. "E001") as the primary key, to match
    # the original project's design. In a bigger production app you'd
    # usually prefer an auto-incrementing integer or UUID as the primary
    # key and keep this as a separate indexed column — but this keeps the
    # migration from the JSON version simple and familiar.
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(String, nullable=True)
