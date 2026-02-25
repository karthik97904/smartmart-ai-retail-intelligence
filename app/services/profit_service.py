from flask import current_app
from app.models.sales import Sale
from app.ai_engine.profit_driver import analyze_profit_drivers
from app import db


def get_profit_driver_report() -> dict:
    """
    Fetches sales data from DB and runs profit driver analysis.
    """
    try:
        sales = Sale.query.all()
        if not sales:
            return {"error": "No sales data found. Ask HR to upload sales data first."}

        sales_data = [
            {
                "product_name": s.product_name,
                "category": s.category,
                "quantity_sold": s.quantity_sold,
                "unit_price": float(s.unit_price),
                "total_revenue": float(s.total_revenue),
                "cost_price": float(s.cost_price),
                "gross_profit": float(s.gross_profit),
                "date": str(s.date)
            }
            for s in sales
        ]

        report = analyze_profit_drivers(sales_data)
        return report

    except Exception as e:
        current_app.logger.error(f"Profit driver service error: {str(e)}")
        return {"error": str(e)}