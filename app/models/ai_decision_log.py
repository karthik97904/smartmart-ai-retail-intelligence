from app.extensions import db
from datetime import datetime


class AIDecisionLog(db.Model):
    __tablename__ = "ai_decision_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action_type = db.Column(db.String(100), nullable=False)
    # executive_analysis / forecast / simulation / risk_index / profit_driver

    input_summary = db.Column(db.Text, nullable=True)
    # JSON string of inputs used

    output_summary = db.Column(db.Text, nullable=True)
    # JSON string of AI output

    confidence_score = db.Column(db.Numeric(6, 2), nullable=True)
    market_stress_score = db.Column(db.Numeric(6, 2), nullable=True)
    risk_index = db.Column(db.Numeric(6, 2), nullable=True)

    execution_time_ms = db.Column(db.Integer, nullable=True)
    # how long AI took in milliseconds

    status = db.Column(db.String(50), default="success")
    # success / failed / partial

    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", back_populates="ai_logs")

    def __repr__(self):
        return f"<AIDecisionLog {self.action_type} confidence:{self.confidence_score}>"