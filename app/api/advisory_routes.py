from flask import Blueprint, jsonify
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.advisory_service import generate_executive_analysis

advisory_bp = Blueprint("advisory", __name__)

@advisory_bp.route("/api/executive-analysis")
@login_required
@role_required("CEO")
def executive_analysis_api():
    result = generate_executive_analysis()
    return jsonify(result)