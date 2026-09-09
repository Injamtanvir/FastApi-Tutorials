# schemas.py
# Pydantic models used for request validation and response shaping.
# Kept separate from models.py (the SQLAlchemy ORM table) on purpose:
# schemas describe "what the API accepts/returns", models describe
# "what's actually stored in the database". This split is a very common
# production pattern (sometimes called Model/Schema or DTO separation).

from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class ExpenseBase(BaseModel):
    name: str = Field(..., description="The name of the expense", examples=["Lunch"])
    amount: float = Field(..., gt=0, description="The amount of the expense", examples=[100.0])
    date: str = Field(..., description="The date of the expense (YYYY-MM-DD)", examples=["2023-01-01"])
    category: str = Field(..., description="The category of the expense", examples=["Food"])
    description: Optional[str] = Field(None, description="A short description", examples=["Lunch at restaurant"])


class ExpenseCreate(ExpenseBase):
    id: str = Field(..., description="The unique ID of the expense", examples=["E001"])


class ExpenseUpdate(BaseModel):
    name: Optional[str] = Field(None, examples=["Lunch"])
    amount: Optional[float] = Field(None, gt=0, examples=[100.0])
    date: Optional[str] = Field(None, examples=["2023-01-01"])
    category: Optional[str] = Field(None, examples=["Food"])
    description: Optional[str] = Field(None, examples=["Lunch at restaurant"])


class ExpenseOut(ExpenseBase):
    id: str

    # Lets Pydantic build this schema directly from a SQLAlchemy object
    # (e.g. `ExpenseOut.model_validate(db_expense)`), not just from a dict.
    model_config = ConfigDict(from_attributes=True)
