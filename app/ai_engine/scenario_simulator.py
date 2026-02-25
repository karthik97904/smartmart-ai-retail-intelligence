def run_simulation(
    base_revenue,
    base_profit,
    price_change_percent,
    demand_change_percent,
    cost_change_percent,
    new_product_revenue,
    expense_reduction_percent
):
    """
    Pure financial simulation logic.
    No DB calls. No Flask imports.
    """

    base_revenue = base_revenue or 0
    base_profit = base_profit or 0

    # --------------------------
    # Revenue Adjustment
    # --------------------------
    revenue_after_price = base_revenue * (1 + price_change_percent / 100)
    revenue_after_demand = revenue_after_price * (1 + demand_change_percent / 100)
    revenue_final = revenue_after_demand + new_product_revenue

    # --------------------------
    # Cost / Profit Adjustment
    # --------------------------
    cost_estimate = base_revenue - base_profit

    cost_after_change = cost_estimate * (1 + cost_change_percent / 100)
    cost_after_reduction = cost_after_change * (1 - expense_reduction_percent / 100)

    projected_profit = revenue_final - cost_after_reduction

    profit_margin = (
        projected_profit / revenue_final
        if revenue_final else 0
    )

    return {
        "projected_revenue": round(revenue_final, 2),
        "projected_profit": round(projected_profit, 2),
        "projected_margin": round(profit_margin * 100, 2)
    }