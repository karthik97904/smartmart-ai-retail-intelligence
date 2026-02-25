from app.services.stress_service import generate_market_stress
from app.services.risk_service import generate_risk_index
from app.services.analytics_service import get_business_summary
from app.ai_engine.decision_brain import generate_advisory


def generate_executive_analysis():

    stress_data = generate_market_stress()
    risk_data = generate_risk_index()
    analytics = get_business_summary()

    financials = analytics["financials"] if analytics else {}

    total_revenue = financials.get("total_revenue", 0)
    net_profit = financials.get("net_profit", 0)

    context = {
        "market_stress": stress_data.get("stress_score", 0),
        "top_driver": stress_data.get("top_driver", "unknown"),
        "risk_data": risk_data,
        "total_revenue": total_revenue,   # ✅ FIXED
        "net_profit": net_profit          # ✅ FIXED
    }

    return generate_advisory(context)