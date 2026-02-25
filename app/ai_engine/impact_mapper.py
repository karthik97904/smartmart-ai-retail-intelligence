from collections import defaultdict

SEVERITY_WEIGHTS = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

CATEGORY_WEIGHTS = {
    "fuel_price": 0.25,
    "inflation": 0.25,
    "supply_chain": 0.20,
    "gst_tax": 0.15,
    "retail_performance": 0.15,
    "other": 0.05
}


def compute_market_stress(news_items):
    """
    news_items: list of NewsCache ORM objects
    returns: dict with stress score and metadata
    """

    if not news_items:
        return {
            "stress_score": 0.0,
            "stress_level": "Low",
            "top_driver": None,
            "event_count": 0
        }

    total_score = 0
    category_accumulator = defaultdict(float)

    for item in news_items:
        severity_weight = SEVERITY_WEIGHTS.get(item.severity, 1)
        category_weight = CATEGORY_WEIGHTS.get(item.category, 0.05)

        weighted_score = severity_weight * category_weight
        total_score += weighted_score
        category_accumulator[item.category] += weighted_score

    # Theoretical maximum (if all events were critical with highest category weight)
    max_possible = len(news_items) * (4 * 0.25)

    normalized_score = round(min(total_score / max_possible, 1.0), 2)

    if normalized_score < 0.25:
        level = "Low"
    elif normalized_score < 0.5:
        level = "Moderate"
    elif normalized_score < 0.75:
        level = "High"
    else:
        level = "Critical"

    top_driver = max(category_accumulator, key=category_accumulator.get)

    return {
        "stress_score": normalized_score,
        "stress_level": level,
        "top_driver": top_driver,
        "event_count": len(news_items)
    }