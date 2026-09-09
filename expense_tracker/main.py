# main.py
# InjamTanvir (INJAM UL HAQUE)
#
# Same routes and behaviour as the original JSON-file version, but every
# route now talks to a real database (Postgres in production, SQLite by
# default locally) through SQLAlchemy instead of reading/writing a JSON file.

from typing import List
from fastapi import FastAPI, HTTPException, Path, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc

from database import Base, engine, get_db
import models
import schemas

# Creates all tables defined in models.py if they don't exist yet.
# This runs once when the app starts up. It's the simplest way to get a
# schema into place; a real production project would eventually swap this
# for migrations (e.g. Alembic) so schema changes are tracked and
# reversible — but this is the right level of complexity for a first
# deployed project.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expense Tracker API",
    description="A simple CRUD API for tracking personal expenses, backed by PostgreSQL.",
    version="1.0.0",
)

# Allows the API to be called from a browser-based frontend on a different
# origin (e.g. a React app on Vercel/Netlify). Tighten allow_origins to
# your actual frontend URL once you have one.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Simple health check — useful for Render to confirm the app is alive."""
    return {"status": "ok", "message": "Expense Tracker API is running"}


@app.get("/view", response_model=List[schemas.ExpenseOut])
def view_expenses(db: Session = Depends(get_db)):
    return db.query(models.Expense).all()


@app.get("/view/{expense_id}", response_model=schemas.ExpenseOut)
def view_specific_expense(
    expense_id: str = Path(..., description="The ID of the expense to retrieve", examples=["E001"]),
    db: Session = Depends(get_db),
):
    expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")
    return expense


@app.get("/sort", response_model=List[schemas.ExpenseOut])
def view_sorted_expenses(
    sorted_by: str = Query(..., description="Field to sort by: name, amount, date, or category"),
    order: str = Query("asc", description="asc or desc"),
    db: Session = Depends(get_db),
):
    valid_fields = {"name", "amount", "date", "category"}
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"sorted_by must be one of {valid_fields}")

    column = getattr(models.Expense, sorted_by)
    direction = desc if order == "desc" else asc
    return db.query(models.Expense).order_by(direction(column)).all()


@app.post("/create", response_model=schemas.ExpenseOut, status_code=201)
def create_expense(expense: schemas.ExpenseCreate, db: Session = Depends(get_db)):
    existing = db.query(models.Expense).filter(models.Expense.id == expense.id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Expense ID already exists")

    db_expense = models.Expense(**expense.model_dump())
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)  # refresh() pulls back any DB-generated values
    return db_expense


@app.put("/edit/{expense_id}", response_model=schemas.ExpenseOut)
def update_expense(expense_id: str, expense: schemas.ExpenseUpdate, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    # Only overwrite fields the client actually sent — same idea as the
    # original exclude_unset=True trick, just applied to an ORM object
    # instead of a dict.
    for field, value in expense.model_dump(exclude_unset=True).items():
        setattr(db_expense, field, value)

    db.commit()
    db.refresh(db_expense)
    return db_expense


@app.delete("/delete/{expense_id}")
def delete_expense(expense_id: str, db: Session = Depends(get_db)):
    db_expense = db.query(models.Expense).filter(models.Expense.id == expense_id).first()
    if not db_expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(db_expense)
    db.commit()
    return {"message": "Expense deleted successfully"}


# Local dev:  uvicorn main:app --reload
# Docs:       http://127.0.0.1:8000/docs
# Root Project folder .venv Activated 'source .venv/bin/activate'