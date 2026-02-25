from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required
from app.utils.decorators import role_required
from app.services.analytics_service import get_business_summary
from app.services.profit_service import get_profit_driver_report
from app.services.forecast_service import generate_forecast
from app.ai_engine.executive_chatbot import generate_ceo_response
from app.services.risk_service import generate_risk_index
from app.services.stress_service import generate_market_stress

ceo_bp = Blueprint("ceo", __name__)

# =========================
# DASHBOARD
# =========================
@ceo_bp.route("/dashboard")
@login_required
@role_required("CEO")
def dashboard():
    return render_template("ceo/dashboard.html")


# =========================
# ANALYTICS
# =========================
@ceo_bp.route("/analytics")
@login_required
@role_required("CEO")
def analytics():
    summary = get_business_summary()
    return render_template("ceo/analytics.html", data=summary)


# =========================
# PROFIT DRIVER
# =========================
@ceo_bp.route("/profit-driver")
@login_required
@role_required("CEO")
def profit_driver():
    report = get_profit_driver_report()
    return render_template("ceo/profit_driver.html", report=report)


# =========================
# FORECAST
# =========================
@ceo_bp.route("/forecast", methods=["GET", "POST"])
@login_required
@role_required("CEO")
def forecast():
    period_type = "monthly"
    periods = 6

    if request.method == "POST":
        period_type = request.form.get("period_type", "monthly")
        periods = int(request.form.get("periods", 6))

    result = generate_forecast(period_type=period_type, periods=periods)

    return render_template(
        "ceo/forecast.html",
        result=result,
        period_type=period_type,
        periods=periods
    )


# =========================
# CHAT UI (KEEP THIS)
# =========================
@ceo_bp.route("/chat-ui")
@login_required
@role_required("CEO")
def chat_ui():
    return render_template("ceo/chat.html")


# =========================
# CHAT API
# =========================
@ceo_bp.route("/chat", methods=["POST"])
@login_required
@role_required("CEO")
def ceo_chat():

    data = request.get_json()

    if not data or "message" not in data:
        return jsonify({"response": "No message provided"}), 400

    question = data["message"]

    result = generate_forecast(period_type="monthly", periods=3)

    response = generate_ceo_response(question, result)

    return jsonify({"response": response})

    # =========================
# DASHBOARD API - ANALYTICS
# =========================
@ceo_bp.route("/api/analytics")
@login_required
@role_required("CEO")
def api_analytics():
    summary = get_business_summary()
    return jsonify(summary)


# =========================
# MARKET STRESS API
# =========================
@ceo_bp.route("/api/market-stress")
@login_required
@role_required("CEO")
def api_market_stress():
    stress_data = generate_market_stress()
    return jsonify(stress_data)

# =========================
# RISK INDEX API
# =========================
@ceo_bp.route("/api/risk-index")
@login_required
@role_required("CEO")
def api_risk_index():

    risk_data = generate_risk_index()

    return jsonify(risk_data)

# =========================
# FORECAST API
# =========================
@ceo_bp.route("/api/forecast")
@login_required
@role_required("CEO")
def api_forecast():
    period_type = request.args.get("period_type", "monthly")
    periods = int(request.args.get("periods", 6))

    result = generate_forecast(period_type=period_type, periods=periods)
    return jsonify(result)