import requests
from app.services.market_service import get_market_intelligence
from app.services.risk_service import generate_risk_index


def call_local_llm(prompt):

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]


def generate_ceo_response(user_question, forecast_result):

    # Internal Forecast Data
    summary = forecast_result.get("summary", {})
    total_revenue = summary.get("total_forecast_revenue")
    total_profit = summary.get("total_forecast_profit")
    trend = summary.get("trend_direction")
    confidence = summary.get("confidence_level")
    accuracy = summary.get("accuracy_score")

    # 🔥 External Market Intelligence
    market_data = get_market_intelligence()
    risk_data = generate_risk_index()

    market_stress = market_data.get("stress_score")
    market_sentiment = market_data.get("overall_sentiment")
    risk_score = risk_data.get("risk_index")
    risk_level = risk_data.get("risk_level")

    prompt = f"""
You are SmartMart AI Advisor.

Your job is to give clear and simple advice.

VERY IMPORTANT RULES:
- Use very simple English.
- Write short and clear sentences.
- Do not explain logic theory.
- Do not use complex business words.
- Do not repeat the question.
- Always start with:
  "Welcome CEO. From the data of SmartMart and today's market,"

Internal SmartMart Data:
Revenue Trend: {trend}
Forecast Revenue: {total_revenue}
Forecast Profit: {total_profit}
Confidence Level: {confidence}
Model Accuracy: {accuracy}%

External Market Data:
Market Sentiment: {market_sentiment}
Market Stress Score: {market_stress}
Risk Score: {risk_score}
Risk Level: {risk_level}

CEO Question:
{user_question}

Respond exactly in this format:

Welcome CEO. From the data of SmartMart and today's market,

Decision:
(Simple clear decision: Expand / Delay / Be Careful)

Reason:
(Explain in simple English why)

What You Should Do:
1.
2.
3.
"""

    return call_local_llm(prompt)