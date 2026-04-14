"""
Feature 8 — Fix-it Content Recommendations
For any result with a low GEO Score (<= 5) or negative Sentiment,
calls the LLM to generate a specific, actionable content brief
that would improve how AI models perceive the brand on that question.
"""
from utils.llm_handler import query_llm


RECOMMENDATION_PROMPT = """You are a GEO (Generative Engine Optimisation) strategist.

A brand called "{client}" received a poor AI perception result for the following question:

QUESTION: {question}
AI RESPONSE: {response}
SENTIMENT: {sentiment}
GEO SCORE: {geo_score}/10
HALLUCINATION RISK: {hallucination_risk}
INDUSTRY: {industry}
COUNTRY: {country}

Write a concise, actionable content brief (3-5 bullet points) that explains:
1. WHAT content {client} should create or update to improve how AI models answer this question
2. WHERE it should be published (e.g. website FAQ, press release, Wikipedia, structured data)
3. WHY this will improve AI perception (cite the specific gap in the response above)

Be specific. Name content types, page types, and formats. Do not give generic SEO advice.
"""


def generate_recommendation(
    result: dict,
    client_name: str,
    industry: str,
    country: str,
    provider: str,
    api_key: str,
    model: str | None = None,
) -> str:
    """
    Generates a content recommendation for a single low-scoring result.
    Returns the recommendation text or an error string.
    """
    prompt = RECOMMENDATION_PROMPT.format(
        client=client_name,
        question=result.get("Question", ""),
        response=result.get("Response", "")[:800],
        sentiment=result.get("Sentiment", "Neutral"),
        geo_score=result.get("GEO Score", "5"),
        hallucination_risk=result.get("Hallucination Risk", "Low"),
        industry=industry,
        country=country,
    )

    res = query_llm(provider, api_key, prompt, model=model)
    if res.get("error"):
        return f"Could not generate recommendation: {res['error']}"
    return res.get("text", "No recommendation generated.")


def should_flag_for_recommendation(result: dict) -> bool:
    """Returns True if a result is worth generating a fix-it brief for."""
    try:
        geo = int(result.get("GEO Score", "5"))
    except (ValueError, TypeError):
        geo = 5
    sentiment = result.get("Sentiment", "Neutral").lower()
    risk = result.get("Hallucination Risk", "Low").lower()
    return geo <= 5 or sentiment == "negative" or risk == "high"
