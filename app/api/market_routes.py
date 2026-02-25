from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.decorators import role_required
from app.repositories.news_repo import get_recent_news

market_bp = Blueprint("market", __name__)

@market_bp.route("/ceo/market-intel")
@login_required
@role_required("CEO")
def market_intel():
    news = get_recent_news()
    return render_template("ceo/market_intel.html", news=news)