from app.repositories.news_repo import get_recent_news
from app.ai_engine.impact_mapper import compute_market_stress


def generate_market_stress():
    # Get last 50 news events
    news_items = get_recent_news(limit=50)

    result = compute_market_stress(news_items)

    return result