from flask import current_app
from app.repositories.analytics_repo import (
    get_total_revenue, get_total_profit,
    get_total_expenses, get_total_units_sold,
    get_top_products, get_category_performance,
    get_monthly_trend, get_low_stock_items,
    get_expense_by_category, get_employee_kpi_summary,
    get_profit_margin, get_sales_count
)


def get_business_summary():
    """
    Returns complete internal business analytics summary.
    Used by CEO dashboard and Executive Advisory Engine.
    """
    try:
        revenue = get_total_revenue()
        profit = get_total_profit()
        expenses = get_total_expenses()
        net_profit = profit - expenses
        margin = get_profit_margin()

        summary = {
            "financials": {
                "total_revenue": revenue,
                "total_gross_profit": profit,
                "total_expenses": expenses,
                "net_profit": net_profit,
                "profit_margin_percent": margin,
                "total_units_sold": get_total_units_sold(),
                "total_transactions": get_sales_count()
            },
            "top_products": get_top_products(5),
            "category_performance": get_category_performance(),
            "monthly_trend": get_monthly_trend(),
            "low_stock_alerts": get_low_stock_items(5),
            "expense_breakdown": get_expense_by_category(),
            "employee_kpis": get_employee_kpi_summary()
        }

        current_app.logger.info("Business analytics summary generated.")
        return summary

    except Exception as e:
        current_app.logger.error(f"Analytics error: {str(e)}")
        return None