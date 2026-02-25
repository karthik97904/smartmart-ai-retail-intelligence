from app.services.analytics_service import get_business_summary
from app.services.risk_service import generate_risk_index
from app.ai_engine.scenario_simulator import run_simulation
from app.models.simulation import Simulation
from app.extensions import db


def generate_simulation(params, user_id):

    analytics = get_business_summary()
    financials = analytics["financials"] if analytics else {}

    base_revenue = financials.get("total_revenue", 0)
    base_profit = financials.get("net_profit", 0)

    simulation_result = run_simulation(
        base_revenue,
        base_profit,
        params.get("price_change_percent", 0),
        params.get("demand_change_percent", 0),
        params.get("cost_change_percent", 0),
        params.get("new_product_revenue", 0),
        params.get("expense_reduction_percent", 0)
    )

    risk_data = generate_risk_index()

    recommendation = (
        "Scenario increases profitability."
        if simulation_result["projected_profit"] > base_profit
        else "Scenario may reduce profitability. Evaluate carefully."
    )

    # ✅ Save to DB (INSIDE FUNCTION)
    simulation_record = Simulation(
        user_id=user_id,
        scenario_name="CEO Scenario Test",
        input_parameters=str(params),
        output_results=str(simulation_result),
        recommendation=recommendation
    )

    db.session.add(simulation_record)
    db.session.commit()

    return {
        "baseline_revenue": base_revenue,
        "baseline_profit": base_profit,
        "simulation": simulation_result,
        "risk_level": risk_data["risk_level"],
        "recommendation": recommendation
    }