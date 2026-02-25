from apscheduler.schedulers.background import BackgroundScheduler
from app.scheduler.jobs import refresh_market_news


def start_scheduler(app):
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=lambda: refresh_market_news(app),
        trigger="interval",
        hours=1,
        id="market_news_refresh",
        replace_existing=True
    )
    scheduler.start()
    app.logger.info("APScheduler started.")