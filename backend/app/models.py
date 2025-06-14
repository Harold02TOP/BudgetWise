from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime
from app.database import Base
from datetime import datetime

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)  # 'income' or 'expense'
    amount = Column(Float)
    category = Column(String)
    date = Column(DateTime, default=datetime.utcnow)
    tags = Column(String, nullable=True)

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(String, unique=True, index=True)  # Format: YYYY-MM
    amount = Column(Float)

class Reminder(Base):
    __tablename__ = "reminders"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    amount = Column(Float)
    due_date = Column(DateTime)
    is_notified = Column(Boolean, default=False)