from app.services.stress_service import generate_market_stress
from app.services.analytics_service import get_business_summary
from app.ai_engine.risk_index import compute_risk_index


def generate_risk_index():

    # 1️⃣ Market Stress
    stress_data = generate_market_stress()
    market_stress = stress_data["stress_score"]

    # 2️⃣ Internal Business Summary
    summary = get_business_summary()

    if not summary:
        return compute_risk_index(
            market_stress,
            0.3, 0.2, 0.2, 0.25
        )

    financials = summary["financials"]

    total_revenue = financials.get("total_revenue", 1) or 1
    net_profit = financials.get("net_profit", 0)
    total_expenses = financials.get("total_expenses", 0)

    expense_ratio = total_expenses / total_revenue
    expense_ratio_risk = min(expense_ratio, 1)

    profit_margin = net_profit / total_revenue
    margin_risk = min(1 - profit_margin, 1)

    low_stock_items = summary.get("low_stock_alerts", [])
    total_products = len(summary.get("category_performance", [])) or 1
    inventory_risk = min(len(low_stock_items) / total_products, 1)

    monthly_trend = summary.get("monthly_trend", [])
    if len(monthly_trend) >= 2:
        revenue_trend_risk = (
            0.6 if monthly_trend[-1]["revenue"] < monthly_trend[-2]["revenue"]
            else 0.2
        )
    else:
        revenue_trend_risk = 0.2

    return compute_risk_index(
        market_stress,
        margin_risk,
        inventory_risk,
        revenue_trend_risk,
        expense_ratio_risk
    )