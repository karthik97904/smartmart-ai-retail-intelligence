import pandas as pd
import numpy as np
from flask import current_app


def analyze_profit_drivers(sales_data: list) -> dict:
    """
    Core AI engine for profit driver analysis.
    Input: list of sale dicts from DB
    Output: structured profit driver report
    """
    if not sales_data:
        return {"error": "No sales data available for analysis."}

    df = pd.DataFrame(sales_data)

    # Ensure numeric types
    df["total_revenue"] = pd.to_numeric(df["total_revenue"], errors="coerce")
    df["gross_profit"] = pd.to_numeric(df["gross_profit"], errors="coerce")
    df["cost_price"] = pd.to_numeric(df["cost_price"], errors="coerce")
    df["quantity_sold"] = pd.to_numeric(df["quantity_sold"], errors="coerce")
    df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")
    df.dropna(subset=["total_revenue", "gross_profit"], inplace=True)

    total_profit = df["gross_profit"].sum()
    total_revenue = df["total_revenue"].sum()

    results = {}

    # 1. Profit contribution by product
    results["product_contribution"] = _product_profit_contribution(df, total_profit)

    # 2. Profit contribution by category
    results["category_contribution"] = _category_profit_contribution(df, total_profit)

    # 3. Margin analysis per product
    results["margin_analysis"] = _margin_analysis(df)

    # 4. Hidden loss makers
    results["hidden_loss_makers"] = _find_hidden_loss_makers(df)

    # 5. Top profit drivers
    results["top_profit_drivers"] = _top_profit_drivers(df)

    # 6. Profit efficiency score per category
    results["efficiency_scores"] = _profit_efficiency(df)

    # 7. Overall health indicators
    results["health"] = {
        "total_revenue": round(float(total_revenue), 2),
        "total_profit": round(float(total_profit), 2),
        "overall_margin": round((total_profit / total_revenue * 100), 2) if total_revenue > 0 else 0,
        "profitable_products": int((df.groupby("product_name")["gross_profit"].sum() > 0).sum()),
        "loss_making_products": int((df.groupby("product_name")["gross_profit"].sum() <= 0).sum()),
    }

    # 8. AI Insight Text
    results["insights"] = _generate_insights(results)

    current_app.logger.info("Profit driver analysis completed.")
    return results


def _product_profit_contribution(df: pd.DataFrame, total_profit: float) -> list:
    grouped = df.groupby("product_name").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum"),
        units=("quantity_sold", "sum")
    ).reset_index()

    grouped["profit_contribution_pct"] = (
        grouped["profit"] / total_profit * 100
    ).round(2)
    grouped["margin_pct"] = (
        grouped["profit"] / grouped["revenue"] * 100
    ).round(2)

    grouped = grouped.sort_values("profit", ascending=False)

    return grouped.head(10).to_dict(orient="records")


def _category_profit_contribution(df: pd.DataFrame, total_profit: float) -> list:
    grouped = df.groupby("category").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum"),
        units=("quantity_sold", "sum")
    ).reset_index()

    grouped["profit_contribution_pct"] = (
        grouped["profit"] / total_profit * 100
    ).round(2)
    grouped["margin_pct"] = (
        grouped["profit"] / grouped["revenue"] * 100
    ).round(2)

    grouped = grouped.sort_values("profit", ascending=False)
    return grouped.to_dict(orient="records")


def _margin_analysis(df: pd.DataFrame) -> list:
    """Finds products with low margin — potential margin erosion."""
    grouped = df.groupby("product_name").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum")
    ).reset_index()

    grouped["margin_pct"] = (
        grouped["profit"] / grouped["revenue"] * 100
    ).round(2)

    # Flag low margin products (below 10%)
    grouped["margin_status"] = grouped["margin_pct"].apply(
        lambda x: "critical" if x < 5 else ("low" if x < 10 else ("healthy" if x < 25 else "excellent"))
    )

    grouped = grouped.sort_values("margin_pct", ascending=True)
    return grouped.head(10).to_dict(orient="records")


def _find_hidden_loss_makers(df: pd.DataFrame) -> list:
    """
    High revenue but low profit products.
    These look good on top line but hurt bottom line.
    """
    grouped = df.groupby("product_name").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum")
    ).reset_index()

    grouped["margin_pct"] = (
        grouped["profit"] / grouped["revenue"] * 100
    ).round(2)

    # High revenue (top 50%) but low margin (below 15%)
    revenue_threshold = grouped["revenue"].quantile(0.5)
    hidden = grouped[
        (grouped["revenue"] >= revenue_threshold) &
        (grouped["margin_pct"] < 15)
    ].sort_values("revenue", ascending=False)

    return hidden.to_dict(orient="records")


def _top_profit_drivers(df: pd.DataFrame) -> list:
    """Top 5 products contributing most to profit."""
    grouped = df.groupby("product_name").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum"),
        units=("quantity_sold", "sum")
    ).reset_index()

    grouped["margin_pct"] = (
        grouped["profit"] / grouped["revenue"] * 100
    ).round(2)

    return grouped.nlargest(5, "profit").to_dict(orient="records")


def _profit_efficiency(df: pd.DataFrame) -> list:
    """
    Profit efficiency = profit per unit sold per category.
    Higher = more efficient category.
    """
    grouped = df.groupby("category").agg(
        profit=("gross_profit", "sum"),
        units=("quantity_sold", "sum"),
        revenue=("total_revenue", "sum")
    ).reset_index()

    grouped["profit_per_unit"] = (
        grouped["profit"] / grouped["units"]
    ).round(2)

    grouped["efficiency_score"] = (
        grouped["profit_per_unit"] /
        grouped["profit_per_unit"].max() * 100
    ).round(2)

    grouped["efficiency_label"] = grouped["efficiency_score"].apply(
        lambda x: "🟢 High" if x >= 70 else ("🟡 Medium" if x >= 40 else "🔴 Low")
    )

    return grouped.sort_values("efficiency_score", ascending=False).to_dict(orient="records")


def _generate_insights(results: dict) -> list:
    """Rule-based AI insight generator."""
    insights = []

    health = results.get("health", {})
    margin = health.get("overall_margin", 0)
    loss_makers = health.get("loss_making_products", 0)
    hidden = results.get("hidden_loss_makers", [])
    top_drivers = results.get("top_profit_drivers", [])

    # Margin insight
    if margin < 10:
        insights.append({
            "type": "critical",
            "message": f"Overall profit margin is critically low at {margin}%. Immediate cost review required."
        })
    elif margin < 20:
        insights.append({
            "type": "warning",
            "message": f"Profit margin at {margin}% is below healthy retail benchmark of 20%. Review pricing."
        })
    else:
        insights.append({
            "type": "positive",
            "message": f"Profit margin at {margin}% is healthy. Focus on scaling top performers."
        })

    # Loss makers
    if loss_makers > 0:
        insights.append({
            "type": "warning",
            "message": f"{loss_makers} product(s) are loss-making. Consider discontinuing or repricing."
        })

    # Hidden loss makers
    if hidden:
        names = ", ".join([h["product_name"] for h in hidden[:3]])
        insights.append({
            "type": "warning",
            "message": f"Hidden margin risk detected in: {names}. High revenue but low profit."
        })

    # Top drivers
    if top_drivers:
        top = top_drivers[0]["product_name"]
        insights.append({
            "type": "positive",
            "message": f"'{top}' is your strongest profit driver. Prioritize its availability and promotion."
        })

    return insights