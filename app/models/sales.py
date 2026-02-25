from app.extensions import db
from datetime import datetime


class Sale(db.Model):
    __tablename__ = "sales"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    product_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    quantity_sold = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_revenue = db.Column(db.Numeric(12, 2), nullable=False)
    cost_price = db.Column(db.Numeric(10, 2), nullable=False)
    gross_profit = db.Column(db.Numeric(12, 2), nullable=False)
    region = db.Column(db.String(100), nullable=True)
    store_id = db.Column(db.String(50), nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale {self.product_name} on {self.date}>"