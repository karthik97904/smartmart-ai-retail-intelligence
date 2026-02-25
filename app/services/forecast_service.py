from flask import current_app
from flask_login import current_user
from app.models.sales import Sale
from app.ai_engine.sales_forecaster import run_forecast
from app.repositories.forecast_repo import save_forecast


def generate_forecast(period_type: str = "monthly", periods: int = 6) -> dict:
    """
    Fetches sales data, runs forecast engine, saves result.
    """
    try:
        sales = Sale.query.all()
        if not sales:
            return {"error": "No sales data found. Ask HR to upload data first."}

        sales_data = [
            {
                "date": str(s.date),
                "total_revenue": float(s.total_revenue),
                "gross_profit": float(s.gross_profit),
                "quantity_sold": s.quantity_sold,
                "category": s.category,
                "product_name": s.product_name
            }
            for s in sales
        ]

        result = run_forecast(sales_data, periods=periods, period_type=period_type)

        if "error" not in result:
            save_forecast(
                user_id=current_user.id,
                forecast_type="revenue",
                period=period_type,
                forecast_data=result,
                accuracy=result.get("accuracy_score", 0),
                seasonal=result.get("seasonal_adjustment", False)
            )
            current_app.logger.info(
                f"Forecast generated: {period_type} | accuracy: {result.get('accuracy_score')}%"
            )

        return result

    except Exception as e:
        current_app.logger.error(f"Forecast service error: {str(e)}")
        return {"error": str(e)}