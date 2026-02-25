from flask import Blueprint, jsonify
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.stress_service import generate_market_stress

stress_bp = Blueprint("stress", __name__)

@stress_bp.route("/ceo/api/market-stress")
@login_required
@role_required("CEO")
def market_stress_api():
    result = generate_market_stress()
    return jsonify(result)