import os
import pandas as pd
from datetime import datetime
from flask import current_app
from werkzeug.utils import secure_filename

from app import db
from app.models.sales import Sale
from app.models.inventory import Inventory
from app.models.employee import Employee
from app.models.expense import Expense
from app.utils.csv_validator import validate_file
from app.utils.validators import allowed_file


def handle_upload(file, data_type: str, uploaded_by: int):
    """
    Main entry point for file upload.
    Returns (success: bool, message: str, row_count: int)
    """
    if not file or file.filename == "":
        return False, "No file selected.", 0

    if not allowed_file(file.filename):
        return False, "Invalid file type. Only CSV, XLSX, XLS allowed.", 0

    filename = secure_filename(file.filename)
    upload_folder = current_app.config.get("UPLOAD_FOLDER", "uploads")
    os.makedirs(upload_folder, exist_ok=True)
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    try:
        df = read_file(filepath)
    except Exception as e:
        return False, f"Could not read file: {str(e)}", 0

    # Normalize columns
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # Validate
    is_valid, errors = validate_file(df, data_type)
    if not is_valid:
        return False, " | ".join(errors), 0

    # Save to DB
    try:
        row_count = save_to_db(df, data_type, uploaded_by)
        current_app.logger.info(
            f"Upload success: {data_type} | {row_count} rows | user_id:{uploaded_by}"
        )
        return True, f"Successfully uploaded {row_count} records.", row_count
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Upload DB error: {str(e)}")
        return False, f"Database error: {str(e)}", 0
    finally:
        # Clean up temp file
        if os.path.exists(filepath):
            os.remove(filepath)


def read_file(filepath: str) -> pd.DataFrame:
    ext = filepath.rsplit(".", 1)[-1].lower()
    if ext == "csv":
        return pd.read_csv(filepath)
    elif ext in ["xlsx", "xls"]:
        return pd.read_excel(filepath)
    else:
        raise ValueError("Unsupported file format.")


def save_to_db(df: pd.DataFrame, data_type: str, uploaded_by: int) -> int:
    if data_type == "sales":
        return save_sales(df, uploaded_by)
    elif data_type == "inventory":
        return save_inventory(df, uploaded_by)
    elif data_type == "employees":
        return save_employees(df, uploaded_by)
    elif data_type == "expenses":
        return save_expenses(df, uploaded_by)
    else:
        raise ValueError(f"Unknown data type: {data_type}")


def save_sales(df: pd.DataFrame, uploaded_by: int) -> int:
    rows = []
    for _, row in df.iterrows():
        sale = Sale(
            date=pd.to_datetime(row["date"]).date(),
            product_name=str(row["product_name"]),
            category=str(row["category"]),
            quantity_sold=int(row["quantity_sold"]),
            unit_price=float(row["unit_price"]),
            total_revenue=float(row["total_revenue"]),
            cost_price=float(row["cost_price"]),
            gross_profit=float(row["gross_profit"]),
            region=str(row.get("region", "")) or None,
            store_id=str(row.get("store_id", "")) or None,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.utcnow()
        )
        rows.append(sale)
    db.session.bulk_save_objects(rows)
    db.session.commit()
    return len(rows)


def save_inventory(df: pd.DataFrame, uploaded_by: int) -> int:
    rows = []
    for _, row in df.iterrows():
        # Check if SKU already exists — update if yes
        existing = Inventory.query.filter_by(sku=str(row["sku"])).first()
        if existing:
            existing.current_stock = int(row["current_stock"])
            existing.unit_cost = float(row["unit_cost"])
            existing.uploaded_at = datetime.utcnow()
        else:
            inv = Inventory(
                product_name=str(row["product_name"]),
                category=str(row["category"]),
                sku=str(row["sku"]),
                current_stock=int(row["current_stock"]),
                reorder_level=int(row.get("reorder_level", 50)),
                unit_cost=float(row["unit_cost"]),
                supplier_name=str(row.get("supplier_name", "")) or None,
                uploaded_by=uploaded_by,
                uploaded_at=datetime.utcnow()
            )
            rows.append(inv)
    if rows:
        db.session.bulk_save_objects(rows)
    db.session.commit()
    return len(df)


def save_employees(df: pd.DataFrame, uploaded_by: int) -> int:
    rows = []
    for _, row in df.iterrows():
        existing = Employee.query.filter_by(
            employee_code=str(row["employee_code"])
        ).first()
        if existing:
            existing.salary = float(row["salary"])
            existing.department = str(row["department"])
            existing.designation = str(row["designation"])
            existing.uploaded_at = datetime.utcnow()
        else:
            emp = Employee(
                employee_code=str(row["employee_code"]),
                full_name=str(row["full_name"]),
                department=str(row["department"]),
                designation=str(row["designation"]),
                salary=float(row["salary"]),
                sales_target=float(row["sales_target"]) if "sales_target" in row and pd.notnull(row.get("sales_target")) else None,
                sales_achieved=float(row["sales_achieved"]) if "sales_achieved" in row and pd.notnull(row.get("sales_achieved")) else None,
                attendance_percent=float(row["attendance_percent"]) if "attendance_percent" in row and pd.notnull(row.get("attendance_percent")) else None,
                uploaded_by=uploaded_by,
                uploaded_at=datetime.utcnow()
            )
            rows.append(emp)
    if rows:
        db.session.bulk_save_objects(rows)
    db.session.commit()
    return len(df)


def save_expenses(df: pd.DataFrame, uploaded_by: int) -> int:
    rows = []
    for _, row in df.iterrows():
        exp = Expense(
            date=pd.to_datetime(row["date"]).date(),
            category=str(row["category"]),
            description=str(row.get("description", "")) or None,
            amount=float(row["amount"]),
            department=str(row.get("department", "")) or None,
            approved_by=str(row.get("approved_by", "")) or None,
            uploaded_by=uploaded_by,
            uploaded_at=datetime.utcnow()
        )
        rows.append(exp)
    db.session.bulk_save_objects(rows)
    db.session.commit()
    return len(rows)