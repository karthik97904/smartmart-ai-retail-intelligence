from app.extensions import db
from datetime import datetime


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)
    employee_code = db.Column(db.String(50), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Numeric(10, 2), nullable=False)
    sales_target = db.Column(db.Numeric(12, 2), nullable=True)
    sales_achieved = db.Column(db.Numeric(12, 2), nullable=True)
    attendance_percent = db.Column(db.Numeric(5, 2), nullable=True)
    joining_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Employee {self.full_name} - {self.department}>"