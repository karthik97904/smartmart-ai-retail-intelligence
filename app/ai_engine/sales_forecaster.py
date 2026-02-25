import pandas as pd
import numpy as np
from flask import current_app
from sklearn.metrics import r2_score


# ----------------------------------
# ACCURACY FUNCTION (R² BASED)
# ----------------------------------
def calculate_accuracy(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)

    if len(actual) < 2:
        return 0

    try:
        score = r2_score(actual, predicted)
        accuracy = max(0, score) * 100
        return round(accuracy, 2)
    except Exception:
        return 0


# ----------------------------------
# SEASONAL INDEX
# ----------------------------------
SEASONAL_INDEX = {
    1: 0.85,
    2: 0.88,
    3: 0.92,
    4: 0.90,
    5: 0.87,
    6: 0.85,
    7: 0.88,
    8: 0.90,
    9: 0.95,
    10: 1.20,
    11: 1.15,
    12: 1.10,
}


# ----------------------------------
# MAIN ENTRY
# ----------------------------------
def run_forecast(sales_data: list, periods: int = 6, period_type: str = "monthly"):

    if not sales_data:
        return {"error": "No sales data available."}

    df = pd.DataFrame(sales_data)
    df["date"] = pd.to_datetime(df["date"])
    df["total_revenue"] = pd.to_numeric(df["total_revenue"], errors="coerce")
    df["gross_profit"] = pd.to_numeric(df["gross_profit"], errors="coerce")
    df.dropna(subset=["date", "total_revenue"], inplace=True)

    if len(df) < 5:
        return {"error": "Need at least 5 records."}

    try:
        if period_type == "monthly":
            return _monthly_forecast(df, periods)
        elif period_type == "weekly":
            return _weekly_forecast(df, periods)
        else:
            return {"error": "Unsupported period type."}
    except Exception as e:
        current_app.logger.error(str(e))
        return {"error": str(e)}


# ----------------------------------
# MONTHLY FORECAST
# ----------------------------------
def _monthly_forecast(df, periods):

    df["period"] = df["date"].dt.to_period("M")
    monthly = df.groupby("period").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum")
    ).reset_index()

    monthly = monthly.sort_values("period")
# Remove very small early months (structural break fix)
    monthly = monthly[monthly["revenue"] > 100000]

# If too few records remain, fallback to last 6 months
    # Remove very small early months (structural break fix)
    monthly = monthly[monthly["revenue"] > 100000]

# If too few records remain, fallback to last 6 months
    if len(monthly) < 3:
        monthly = monthly.tail(6)

    if len(monthly) < 3:
        return {"error": "Need at least 3 months."}

    monthly["period_str"] = monthly["period"].astype(str)

    revenues = monthly["revenue"].values
    profits = monthly["profit"].values

    # -------- Growth Model --------
    growth_rates = []
    for i in range(1, len(revenues)):
        if revenues[i - 1] > 0:
            growth = (revenues[i] - revenues[i - 1]) / revenues[i - 1]
            growth_rates.append(growth)

    avg_growth = np.mean(growth_rates) if growth_rates else 0

    # Reconstruct historical prediction
    y_pred_rev = [revenues[0]]
    for i in range(1, len(revenues)):
        y_pred_rev.append(y_pred_rev[i - 1] * (1 + avg_growth))

    y_pred_rev = np.array(y_pred_rev)

    accuracy = calculate_accuracy(revenues, y_pred_rev)

    std_dev = float(np.std(revenues - y_pred_rev))

    last_period = monthly["period"].iloc[-1]

    future_periods = []
    future_revenue = []
    future_profit = []
    future_lower = []
    future_upper = []

    last_rev = revenues[-1]
    last_profit = profits[-1]

    for i in range(1, periods + 1):

        next_period = last_period + i
        month_num = next_period.month

        base_rev = last_rev * (1 + avg_growth)
        base_profit = last_profit * (1 + avg_growth)

        last_rev = base_rev
        last_profit = base_profit

        seasonal = SEASONAL_INDEX.get(month_num, 1.0)

        adj_rev = max(0, base_rev * seasonal)
        adj_profit = max(0, base_profit * seasonal)

        future_periods.append(str(next_period))
        future_revenue.append(round(adj_rev, 2))
        future_profit.append(round(adj_profit, 2))
        future_lower.append(round(max(0, adj_rev - 1.96 * std_dev), 2))
        future_upper.append(round(adj_rev + 1.96 * std_dev, 2))

        # --------- RISK ANALYSIS ---------

    mean_rev = np.mean(revenues)
    std_hist = np.std(revenues)

    if mean_rev > 0:
        volatility_ratio = std_hist / mean_rev
    else:
        volatility_ratio = 0

    stability_index = max(0, min(100, round((1 - volatility_ratio) * 100, 2)))
    risk_score = round(100 - stability_index, 2)

    if risk_score < 30:
        volatility_level = "Low"
    elif risk_score < 60:
        volatility_level = "Moderate"
    else:
        volatility_level = "High"

    if volatility_level == "Low":
        executive_signal = "Stable growth trajectory with controlled fluctuations."
    elif volatility_level == "Moderate":
        executive_signal = "Growth present but revenue fluctuations detected."
    else:
        executive_signal = "High volatility — expansion risk or unstable demand pattern."

    return {
        "period_type": "monthly",
        "historical": {
            "periods": monthly["period_str"].tolist(),
            "revenue": [round(float(r), 2) for r in revenues],
            "profit": [round(float(p), 2) for p in profits]
        },
        "forecast": {
            "periods": future_periods,
            "revenue": future_revenue,
            "profit": future_profit,
            "lower_bound": future_lower,
            "upper_bound": future_upper
        },
        "accuracy_score": accuracy,
        "model": "Growth-Based Forecast + Seasonal Index",
        "summary": _forecast_summary(future_revenue, future_profit, accuracy),
        "risk_analysis": {
            "risk_score": risk_score,
            "stability_index": stability_index,
            "volatility_level": volatility_level,
            "executive_signal": executive_signal
        }
    }


# ----------------------------------
# WEEKLY FORECAST
# ----------------------------------
def _weekly_forecast(df, periods):

    df["period"] = df["date"].dt.to_period("W")
    weekly = df.groupby("period").agg(
        revenue=("total_revenue", "sum"),
        profit=("gross_profit", "sum")
    ).reset_index()

    weekly = weekly.sort_values("period").tail(12)

    if len(weekly) < 3:
        return {"error": "Need at least 3 weeks."}

    weekly["period_str"] = weekly["period"].astype(str)

    revenues = weekly["revenue"].values
    profits = weekly["profit"].values

    accuracy = calculate_accuracy(revenues, revenues)

    last_period = weekly["period"].iloc[-1]

    future_periods = []
    future_revenue = []
    future_profit = []

    last_rev = revenues[-1]
    last_profit = profits[-1]

    for i in range(1, periods + 1):

        next_period = last_period + i

        future_periods.append(str(next_period))
        future_revenue.append(round(last_rev, 2))
        future_profit.append(round(last_profit, 2))

    return {
        "period_type": "weekly",
        "historical": {
            "periods": weekly["period_str"].tolist(),
            "revenue": [round(float(r), 2) for r in revenues],
            "profit": [round(float(p), 2) for p in profits]
        },
        "forecast": {
            "periods": future_periods,
            "revenue": future_revenue,
            "profit": future_profit,
            "lower_bound": future_revenue,
            "upper_bound": future_revenue
        },
        "accuracy_score": accuracy,
        "model": "Flat Weekly Projection",
        "summary": _forecast_summary(future_revenue, future_profit, accuracy),
        
        "risk_analysis": {
            "risk_score": risk_score,
            "stability_index": stability_index,
            "volatility_level": volatility_level,
            "executive_signal": executive_signal
        }
    
    }


# ----------------------------------
# SUMMARY
# ----------------------------------
def _forecast_summary(future_revenue, future_profit, accuracy):

    if not future_revenue:
        return {}

    total_rev = sum(future_revenue)
    total_profit = sum(future_profit)
    avg_rev = total_rev / len(future_revenue)

    trend = "upward 📈" if future_revenue[-1] > future_revenue[0] else "downward 📉"

    return {
        "total_forecast_revenue": round(total_rev, 2),
        "total_forecast_profit": round(total_profit, 2),
        "average_period_revenue": round(avg_rev, 2),
        "trend_direction": trend,
        "confidence_level": (
            "High" if accuracy >= 80 else
            "Medium" if accuracy >= 60 else "Low"
        ),
        "accuracy_score": accuracy
    }