from app.extensions import db
from datetime import datetime


class Expense(db.Model):
    __tablename__ = "expenses"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    category = db.Column(db.String(100), nullable=False)  # rent, utilities, salaries, etc.
    description = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Numeric(12, 2), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    approved_by = db.Column(db.String(100), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Expense {self.category} - {self.amount} on {self.date}>"