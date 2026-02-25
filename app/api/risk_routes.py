from flask import Blueprint, jsonify
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.risk_service import generate_risk_index

risk_bp = Blueprint("risk", __name__)

@risk_bp.route("/api/risk-index")
@login_required
@role_required("CEO")
def risk_index_api():
    result = generate_risk_index()
    return jsonify(result)