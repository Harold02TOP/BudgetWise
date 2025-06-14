from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TransactionBase(BaseModel):
    type: str
    amount: float
    category: str
    date: datetime
    tags: Optional[str] = None

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int

    class Config:
        from_attributes = True

class BudgetBase(BaseModel):
    month: str  # Format: YYYY-MM
    amount: float

class BudgetCreate(BudgetBase):
    pass

class Budget(BudgetBase):
    id: int

    class Config:
        from_attributes = True

class ReminderBase(BaseModel):
    description: str
    amount: float
    due_date: datetime

class ReminderCreate(ReminderBase):
    pass

class Reminder(ReminderBase):
    id: int
    is_notified: bool

    class Config:
        from_attributes = True