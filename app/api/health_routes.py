from flask import Blueprint
from app.utils.response_helper import success_response

health_bp = Blueprint("health", __name__)


@health_bp.route("/ping", methods=["GET"])
def ping():
    return success_response(message="SmartMart API is running.")