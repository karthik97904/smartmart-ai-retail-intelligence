import json
from app.extensions import db
from app.models.forecast import Forecast


def save_forecast(user_id: int, forecast_type: str, period: str,
                  forecast_data: dict, accuracy: float, seasonal: bool) -> Forecast:
    record = Forecast(
        user_id=user_id,
        forecast_type=forecast_type,
        period=period,
        forecast_data=json.dumps(forecast_data),
        accuracy_score=accuracy,
        seasonal_adjustment=seasonal
    )
    db.session.add(record)
    db.session.commit()
    return record


def get_latest_forecast(forecast_type: str = "revenue", period: str = "monthly"):
    return Forecast.query.filter_by(
        forecast_type=forecast_type,
        period=period
    ).order_by(Forecast.created_at.desc()).first()


def get_all_forecasts(limit: int = 10):
    return Forecast.query.order_by(
        Forecast.created_at.desc()
    ).limit(limit).all()