from app.extensions import db
from datetime import datetime


class Simulation(db.Model):
    __tablename__ = "simulations"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    scenario_name = db.Column(db.String(150), nullable=False)
    input_parameters = db.Column(db.Text, nullable=False)
    # JSON: price_change, demand_shift, cost_change etc.
    output_results = db.Column(db.Text, nullable=False)
    # JSON: projected revenue, profit impact etc.
    recommendation = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="simulations")

    def __repr__(self):
        return f"<Simulation {self.scenario_name}>" 