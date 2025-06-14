from sqlalchemy.orm import Session
from app import models, schemas
from datetime import datetime
from typing import List, Optional

def create_budget(db: Session, budget: schemas.BudgetCreate):
    db_budget = models.Budget(month=budget.month, amount=budget.amount)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget

def get_budget(db: Session, month: str):
    return db.query(models.Budget).filter(models.Budget.month == month).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        type=transaction.type,
        amount=transaction.amount,
        category=transaction.category,
        date=transaction.date,
        tags=transaction.tags
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, skip: int = 0, limit: int = 100, start_date: Optional[str] = None, end_date: Optional[str] = None):
    query = db.query(models.Transaction)
    if start_date and end_date:
        query = query.filter(models.Transaction.date.between(start_date, end_date))
    return query.offset(skip).limit(limit).all()

def update_transaction(db: Session, transaction_id: int, transaction: schemas.TransactionCreate):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db_transaction.type = transaction.type
        db_transaction.amount = transaction.amount
        db_transaction.category = transaction.category
        db_transaction.date = transaction.date
        db_transaction.tags = transaction.tags
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
        return True
    return False

def get_balance(db: Session, month: str):
    transactions = db.query(models.Transaction).filter(
        models.Transaction.date.like(f"{month}%")
    ).all()
    income = sum(t.amount for t in transactions if t.type == "income")
    expense = sum(t.amount for t in transactions if t.type == "expense")
    return income - expense

def create_reminder(db: Session, reminder: schemas.ReminderCreate):
    db_reminder = models.Reminder(
        description=reminder.description,
        amount=reminder.amount,
        due_date=reminder.due_date
    )
    db.add(db_reminder)
    db.commit()
    db.refresh(db_reminder)
    return db_reminder