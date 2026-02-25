import pandas as pd

# Required columns for each data type
REQUIRED_COLUMNS = {
    "sales": [
        "date", "product_name", "category",
        "quantity_sold", "unit_price",
        "total_revenue", "cost_price", "gross_profit"
    ],
    "inventory": [
        "product_name", "category", "sku",
        "current_stock", "reorder_level",
        "unit_cost"
    ],
    "employees": [
        "employee_code", "full_name", "department",
        "designation", "salary"
    ],
    "expenses": [
        "date", "category", "amount"
    ]
}


def validate_file(df: pd.DataFrame, data_type: str):
    """
    Validates a DataFrame against required columns and basic rules.
    Returns (is_valid: bool, errors: list)
    """
    errors = []

    # Normalize column names
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    required = REQUIRED_COLUMNS.get(data_type, [])

    # Check required columns exist
    missing_cols = [col for col in required if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")
        return False, errors

    # Check not empty
    if df.empty:
        errors.append("File contains no data rows.")
        return False, errors

    # Check for completely empty required columns
    for col in required:
        if df[col].isnull().all():
            errors.append(f"Column '{col}' is completely empty.")

    # Type checks per data type
    if data_type == "sales":
        try:
            pd.to_datetime(df["date"])
        except Exception:
            errors.append("Column 'date' has invalid date format. Use YYYY-MM-DD.")

        for num_col in ["quantity_sold", "unit_price", "total_revenue", "cost_price", "gross_profit"]:
            if not pd.to_numeric(df[num_col], errors="coerce").notnull().all():
                errors.append(f"Column '{num_col}' must contain numeric values only.")

    if data_type == "inventory":
        for num_col in ["current_stock", "reorder_level", "unit_cost"]:
            if not pd.to_numeric(df[num_col], errors="coerce").notnull().all():
                errors.append(f"Column '{num_col}' must contain numeric values only.")

    if data_type == "employees":
        if not pd.to_numeric(df["salary"], errors="coerce").notnull().all():
            errors.append("Column 'salary' must contain numeric values only.")

    if data_type == "expenses":
        try:
            pd.to_datetime(df["date"])
        except Exception:
            errors.append("Column 'date' has invalid date format. Use YYYY-MM-DD.")
        if not pd.to_numeric(df["amount"], errors="coerce").notnull().all():
            errors.append("Column 'amount' must contain numeric values only.")

    if errors:
        return False, errors

    return True, []