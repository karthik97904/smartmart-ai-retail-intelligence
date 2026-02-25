def generate_advisory(context):

    market_stress = context.get("market_stress", 0) or 0
    risk_data = context.get("risk_data", {})
    total_revenue = context.get("total_revenue", 0) or 0
    net_profit = context.get("net_profit", 0) or 0
    top_driver = context.get("top_driver", "unknown")

    risk_score = risk_data.get("risk_score", 0) or 0
    risk_level = risk_data.get("risk_level", "Unknown")

    # -----------------------------
    # Executive Summary
    # -----------------------------
    if total_revenue:
        executive_summary = (
            f"SmartMart is currently operating under {risk_level} risk conditions "
            f"with a market stress score of {market_stress}. "
            f"The dominant external driver is {top_driver}. "
            f"Net profit stands at {net_profit} against revenue of {total_revenue}."
        )
    else:
        executive_summary = (
            "SmartMart currently has insufficient revenue data to compute full financial insights."
        )

    # -----------------------------
    # Strategic Recommendations
    # -----------------------------
    strategic_recommendations = []

    if risk_score > 0.6:
        strategic_recommendations.append(
            "Implement cost-control strategy immediately."
        )

    if market_stress > 0.4:
        strategic_recommendations.append(
            "Strengthen supply chain resilience."
        )

    # Safe profit margin calculation
    profit_margin = (net_profit / total_revenue) if total_revenue else 0

    if profit_margin < 0.1:
        strategic_recommendations.append(
            "Re-evaluate pricing and margin structure."
        )

    if not strategic_recommendations:
        strategic_recommendations.append(
            "Maintain current strategic posture with cautious expansion."
        )

    # -----------------------------
    # Tactical Actions
    # -----------------------------
    tactical_actions = [
        "Review top 10 expense categories.",
        "Increase monitoring of low-stock SKUs.",
        "Optimize promotional pricing.",
        "Improve vendor negotiation terms.",
        "Track weekly revenue performance closely."
    ]

    # -----------------------------
    # Risk Alerts
    # -----------------------------
    risk_alerts = [
        f"Overall risk level: {risk_level}",
        f"Primary stress driver: {top_driver}"
    ]

    # -----------------------------
    # Growth Opportunities
    # -----------------------------
    growth_opportunities = []

    if risk_score < 0.4:
        growth_opportunities.append(
            "Expand high-margin product categories."
        )
        growth_opportunities.append(
            "Launch targeted marketing campaigns."
        )

    # -----------------------------
    # Confidence Score (SAFE)
    # -----------------------------
    try:
        confidence_raw = 1 - (abs(risk_score - market_stress) / 2)
        confidence_score = round(max(min(confidence_raw, 1), 0), 2)
    except Exception:
        confidence_score = 0.5

    return {
        "executive_summary": executive_summary,
        "strategic_recommendations": strategic_recommendations,
        "tactical_actions": tactical_actions,
        "risk_alerts": risk_alerts,
        "growth_opportunities": growth_opportunities,
        "confidence_score": confidence_score
    }