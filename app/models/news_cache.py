from app.extensions import db
from datetime import datetime


class NewsCache(db.Model):
    __tablename__ = "news_cache"

    id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String(500), nullable=False)
    source = db.Column(db.String(150), nullable=True)
    url = db.Column(db.String(500), nullable=True)
    published_at = db.Column(db.DateTime, nullable=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)

    # AI Classification Fields
    category = db.Column(db.String(100), nullable=True)
    # fuel_price / gst_tax / inflation / supply_chain / retail_performance / other
    severity = db.Column(db.String(50), nullable=True)
    # low / medium / high / critical
    sentiment_score = db.Column(db.Numeric(5, 4), nullable=True)
    # -1.0 to +1.0
    impact_variable = db.Column(db.String(150), nullable=True)
    # mapped business variable
    is_processed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<NewsCache {self.category} - {self.severity}>"