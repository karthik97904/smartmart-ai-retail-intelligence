from app.extensions import db
from datetime import datetime


class Forecast(db.Model):
    __tablename__ = "forecasts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    forecast_type = db.Column(db.String(100), nullable=False)
    # revenue / units / profit
    period = db.Column(db.String(50), nullable=False)
    # weekly / monthly / quarterly
    forecast_data = db.Column(db.Text, nullable=False)
    # JSON string of forecast values
    accuracy_score = db.Column(db.Numeric(6, 2), nullable=True)
    seasonal_adjustment = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="forecasts")

    def __repr__(self):
        return f"<Forecast {self.forecast_type} - {self.period}>"