import feedparser
from datetime import datetime
from app.ai_engine.market_analyzer import analyze_news_item
from app.repositories.news_repo import headline_exists, save_news

# ---------- RSS FETCHER ----------

RSS_FEEDS = [
    "https://economictimes.indiatimes.com/industry/rssfeeds/13352306.cms",
    "https://www.thehindu.com/business/feeder/default.rss",
    "https://www.livemint.com/rss/economy",
    "https://pib.gov.in/rss.aspx"
]

def fetch_and_process_news():
    for feed_url in RSS_FEEDS:
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            if headline_exists(entry.link):
                continue

            analyzed = analyze_news_item(entry.title)

            news_data = {
                **analyzed,
                "source": feed.feed.get("title", "Unknown"),
                "url": entry.link,
                "published_at": datetime(*entry.published_parsed[:6])
                    if entry.get("published_parsed") else datetime.utcnow(),
                "is_processed": True
            }

            save_news(news_data)

# ---------- MARKET INTELLIGENCE ----------

from app.models import NewsCache
from app.extensions import db
from sqlalchemy import desc

def get_market_intelligence():

    news_items = (
        db.session.query(NewsCache)
        .filter(NewsCache.is_processed == True)
        .order_by(desc(NewsCache.fetched_at))
        .limit(20)
        .all()
    )

    if not news_items:
        return {
            "overall_sentiment": "Neutral",
            "stress_score": 0,
            "dominant_category": "None",
            "severity_level": "low"
        }

    total_sentiment = 0
    severity_counter = {}
    category_counter = {}

    severity_weight = {
        "low": 1,
        "medium": 2,
        "high": 3,
        "critical": 4
    }

    severity_score_sum = 0

    for item in news_items:

        sentiment = float(item.sentiment_score or 0)
        total_sentiment += sentiment

        category = item.category or "other"
        category_counter[category] = category_counter.get(category, 0) + 1

        severity = item.severity or "low"
        severity_counter[severity] = severity_counter.get(severity, 0) + 1
        severity_score_sum += severity_weight.get(severity, 1)

    avg_sentiment = total_sentiment / len(news_items)
    avg_severity_score = severity_score_sum / len(news_items)

    stress_score = round(
        (abs(avg_sentiment) * 50) +
        (avg_severity_score * 12.5), 2
    )

    if avg_sentiment > 0.2:
        overall = "Positive"
    elif avg_sentiment < -0.2:
        overall = "Negative"
    else:
        overall = "Neutral"

    dominant_category = max(category_counter, key=category_counter.get)
    dominant_severity = max(severity_counter, key=severity_counter.get)

    return {
        "overall_sentiment": overall,
        "stress_score": stress_score,
        "dominant_category": dominant_category,
        "severity_level": dominant_severity
    }