from sqlalchemy import func, extract
from app.extensions import db
from app.models.sales import Sale
from app.models.inventory import Inventory
from app.models.employee import Employee
from app.models.expense import Expense


def get_total_revenue():
    result = db.session.query(func.sum(Sale.total_revenue)).scalar()
    return float(result or 0)


def get_total_profit():
    result = db.session.query(func.sum(Sale.gross_profit)).scalar()
    return float(result or 0)


def get_total_expenses():
    result = db.session.query(func.sum(Expense.amount)).scalar()
    return float(result or 0)


def get_total_units_sold():
    result = db.session.query(func.sum(Sale.quantity_sold)).scalar()
    return int(result or 0)


def get_top_products(limit=5):
    results = db.session.query(
        Sale.product_name,
        func.sum(Sale.total_revenue).label("revenue"),
        func.sum(Sale.quantity_sold).label("units")
    ).group_by(Sale.product_name)\
     .order_by(func.sum(Sale.total_revenue).desc())\
     .limit(limit).all()
    return [{"product": r.product_name, "revenue": float(r.revenue), "units": int(r.units)} for r in results]


def get_category_performance():
    results = db.session.query(
        Sale.category,
        func.sum(Sale.total_revenue).label("revenue"),
        func.sum(Sale.gross_profit).label("profit"),
        func.sum(Sale.quantity_sold).label("units")
    ).group_by(Sale.category)\
     .order_by(func.sum(Sale.total_revenue).desc()).all()
    return [
        {
            "category": r.category,
            "revenue": float(r.revenue),
            "profit": float(r.profit),
            "units": int(r.units)
        } for r in results
    ]


def get_monthly_trend():
    results = db.session.query(
        extract("year", Sale.date).label("year"),
        extract("month", Sale.date).label("month"),
        func.sum(Sale.total_revenue).label("revenue"),
        func.sum(Sale.gross_profit).label("profit")
    ).group_by("year", "month")\
     .order_by("year", "month").all()
    return [
        {
            "period": f"{int(r.year)}-{int(r.month):02d}",
            "revenue": float(r.revenue),
            "profit": float(r.profit)
        } for r in results
    ]


def get_low_stock_items(threshold=50):
    results = Inventory.query.filter(
        Inventory.current_stock <= Inventory.reorder_level
    ).all()
    return [
        {
            "product": i.product_name,
            "sku": i.sku,
            "current_stock": i.current_stock,
            "reorder_level": i.reorder_level
        } for i in results
    ]


def get_expense_by_category():
    results = db.session.query(
        Expense.category,
        func.sum(Expense.amount).label("total")
    ).group_by(Expense.category)\
     .order_by(func.sum(Expense.amount).desc()).all()
    return [{"category": r.category, "total": float(r.total)} for r in results]


def get_employee_kpi_summary():
    results = db.session.query(
        Employee.department,
        func.count(Employee.id).label("headcount"),
        func.sum(Employee.salary).label("total_salary"),
        func.avg(Employee.attendance_percent).label("avg_attendance"),
        func.avg(Employee.sales_achieved / Employee.sales_target * 100).label("avg_target_achievement")
    ).filter(Employee.is_active == True)\
     .group_by(Employee.department).all()
    return [
        {
            "department": r.department,
            "headcount": int(r.headcount),
            "total_salary": float(r.total_salary or 0),
            "avg_attendance": round(float(r.avg_attendance or 0), 2),
            "avg_target_achievement": round(float(r.avg_target_achievement or 0), 2)
        } for r in results
    ]


def get_profit_margin():
    revenue = get_total_revenue()
    profit = get_total_profit()
    if revenue == 0:
        return 0.0
    return round((profit / revenue) * 100, 2)


def get_sales_count():
    return db.session.query(func.count(Sale.id)).scalar() or 0