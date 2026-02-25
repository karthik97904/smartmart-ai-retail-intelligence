from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.utils.decorators import role_required
from app.services.simulation_service import generate_simulation

# ✅ Define Blueprint FIRST
simulation_bp = Blueprint("simulation", __name__)


@simulation_bp.route("/ceo/api/simulate", methods=["GET", "POST"])
@login_required
@role_required("CEO")
def simulate():

    if request.method == "POST":
        params = request.get_json()
    else:
        # Default test parameters
        params = {
            "price_change_percent": 5,
            "demand_change_percent": 3,
            "cost_change_percent": 2,
            "new_product_revenue": 100000,
            "expense_reduction_percent": 1
        }

    result = generate_simulation(params, current_user.id)
    return jsonify(result)