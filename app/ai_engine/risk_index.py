def compute_risk_index(
    market_stress,
    margin_risk,
    inventory_risk,
    revenue_trend_risk,
    expense_ratio_risk
):
    risk_score = (
        (market_stress * 0.30)
        + (margin_risk * 0.25)
        + (inventory_risk * 0.20)
        + (revenue_trend_risk * 0.15)
        + (expense_ratio_risk * 0.10)
    )

    risk_score = round(min(risk_score, 1.0), 2)

    if risk_score < 0.25:
        level = "Low"
    elif risk_score < 0.5:
        level = "Moderate"
    elif risk_score < 0.75:
        level = "High"
    else:
        level = "Critical"

    opportunity_score = round(1 - risk_score, 2)

    return {
        "risk_score": risk_score,
        "risk_level": level,
        "opportunity_score": opportunity_score
    }