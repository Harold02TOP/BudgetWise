from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, engine
from app import models
import datetime

client = TestClient(app)

def setup_module():
    models.Base.metadata.create_all(bind=engine)

def teardown_module():
    db = SessionLocal()
    db.query(models.Transaction).delete()
    db.query(models.Budget).delete()
    db.query(models.Reminder).delete()
    db.commit()
    db.close()

def test_create_budget():
    response = client.post("/budgets/", json={"month": "2025-06", "amount": 5000})
    assert response.status_code == 200
    assert response.json()["month"] == "2025-06"
    assert response.json()["amount"] == 5000

def test_create_transaction():
    response = client.post(
        "/transactions/",
        json={
            "type": "income",
            "amount": 1000,
            "category": "Salary",
            "date": "2025-06-01T00:00:00",
            "tags": "recurrent"
        }
    )
    assert response.status_code == 200
    assert response.json()["type"] == "income"
    assert response.json()["amount"] == 1000