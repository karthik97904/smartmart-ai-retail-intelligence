from app.extensions import db
from datetime import datetime


class Inventory(db.Model):
    __tablename__ = "inventory"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False)
    current_stock = db.Column(db.Integer, nullable=False)
    reorder_level = db.Column(db.Integer, nullable=False, default=50)
    unit_cost = db.Column(db.Numeric(10, 2), nullable=False)
    supplier_name = db.Column(db.String(150), nullable=True)
    last_restocked = db.Column(db.Date, nullable=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Inventory {self.product_name} SKU:{self.sku}>"