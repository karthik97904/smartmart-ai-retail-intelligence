from app.services.market_service import fetch_and_process_news

def refresh_market_news():
    fetch_and_process_news()