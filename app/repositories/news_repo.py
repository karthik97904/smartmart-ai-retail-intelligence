from app.models.news_cache import NewsCache
from app.extensions import db

def headline_exists(url):
    return NewsCache.query.filter_by(url=url).first() is not None


def save_news(news_dict):
    news = NewsCache(
        headline=news_dict["headline"],
        source=news_dict["source"],
        url=news_dict["url"],
        published_at=news_dict["published_at"],
        fetched_at=news_dict["fetched_at"],
        category=news_dict["category"],
        severity=news_dict["severity"],
        sentiment_score=news_dict["sentiment_score"],
        impact_variable=news_dict["category"],
        is_processed=False
    )
    db.session.add(news)
    db.session.commit()


def get_recent_news(limit=50):
    return NewsCache.query.order_by(
        NewsCache.published_at.desc()
    ).limit(limit).all()