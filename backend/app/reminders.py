from sqlalchemy.orm import Session
from app import models
from datetime import datetime, timedelta

def check_due_reminders(db: Session):
    now = datetime.utcnow()
    due_date_limit = now + timedelta(hours=24)
    reminders = db.query(models.Reminder).filter(
        models.Reminder.due_date.between(now, due_date_limit),
        models.Reminder.is_notified == False
    ).all()
    for reminder in reminders:
        reminder.is_notified = True
    db.commit()
    return reminders