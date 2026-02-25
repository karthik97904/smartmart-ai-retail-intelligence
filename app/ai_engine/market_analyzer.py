from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from datetime import datetime

analyzer = SentimentIntensityAnalyzer()

CATEGORY_KEYWORDS = {
    "fuel_price": [
        "petrol", "diesel", "crude", "oil price", "fuel", "brent"
    ],
    "gst_tax": [
        "gst", "tax", "tariff", "cess", "duty", "import duty"
    ],
    "inflation": [
        "inflation", "cpi", "wpi", "price rise", "costlier", "food prices"
    ],
    "supply_chain": [
        "shortage", "logistics", "freight", "port",
        "supply chain", "delay", "container", "shipping"
    ],
    "retail_performance": [
        "retail", "fmcg", "footfall", "sales growth",
        "consumer demand", "mall", "store expansion"
    ]
}

SEVERITY_MAP = {
    1: "low",
    2: "medium",
    3: "high",
    4: "critical"
}

def classify_headline(headline: str):
    headline_lower = headline.lower()
    scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        match_count = 0
        for word in keywords:
            if word.lower() in headline_lower:
                match_count += 1

        if match_count > 0:
            scores[category] = match_count

    if not scores:
        # NEW: fallback logic using broad signals
        if "bank" in headline_lower or "finance" in headline_lower:
            return "retail_performance", "low"
        if "import" in headline_lower or "export" in headline_lower:
            return "supply_chain", "low"
        return "other", "low"

    top_category = max(scores, key=scores.get)
    keyword_count = scores[top_category]

    # Improved severity scaling
    if keyword_count >= 3:
        severity = "high"
    elif keyword_count == 2:
        severity = "medium"
    else:
        severity = "low"

    return top_category, severity


def analyze_sentiment(text: str):
    sentiment = analyzer.polarity_scores(text)
    return sentiment["compound"]


def analyze_news_item(headline: str):
    category, severity = classify_headline(headline)
    sentiment_score = analyze_sentiment(headline)

    # Boost severity if sentiment is strongly negative
    if sentiment_score < -0.5:
        severity = "high"
    elif sentiment_score < -0.2 and severity == "low":
        severity = "medium"

    return {
        "headline": headline,
        "category": category,
        "severity": severity,
        "sentiment_score": sentiment_score,
        "fetched_at": datetime.utcnow()
    }