from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import SessionLocal, engine
from app.pdf_generator import generate_pdf_report
from app.reminders import check_due_reminders
from typing import List
import datetime

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/budgets/", response_model=schemas.Budget)
def create_budget(budget: schemas.BudgetCreate, db: Session = Depends(get_db)):
    return crud.create_budget(db=db, budget=budget)

@app.get("/budgets/{month}", response_model=schemas.Budget)
def read_budget(month: str, db: Session = Depends(get_db)):
    db_budget = crud.get_budget(db, month=month)
    if db_budget is None:
        raise HTTPException(status_code=404, detail="Budget not found")
    return db_budget

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.get("/transactions/", response_model=List[schemas.Transaction])
def read_transactions(skip: int = 0, limit: int = 100, start_date: str = None, end_date: str = None, db: Session = Depends(get_db)):
    transactions = crud.get_transactions(db, skip=skip, limit=limit, start_date=start_date, end_date=end_date)
    return transactions

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = crud.update_transaction(db, transaction_id=transaction_id, transaction=transaction)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    success = crud.delete_transaction(db, transaction_id=transaction_id)
    if not success:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": "Transaction deleted"}

@app.get("/balance/{month}")
def get_balance(month: str, db: Session = Depends(get_db)):
    balance = crud.get_balance(db, month=month)
    return {"balance": balance}

@app.post("/reminders/", response_model=schemas.Reminder)
def create_reminder(reminder: schemas.ReminderCreate, db: Session = Depends(get_db)):
    return crud.create_reminder(db=db, reminder=reminder)

@app.get("/reminders/", response_model=List[schemas.Reminder])
def read_reminders(db: Session = Depends(get_db)):
    reminders = check_due_reminders(db)
    return reminders

@app.get("/report/{month}")
def generate_report(month: str, db: Session = Depends(get_db)):
    budget = crud.get_budget(db, month=month)
    transactions = crud.get_transactions(db, start_date=f"{month}-01", end_date=f"{month}-31")
    filename = f"report_{month}.pdf"
    generate_pdf_report(month, budget.amount if budget else 0, transactions, filename)
    return {"message": f"Report generated at {filename}"}