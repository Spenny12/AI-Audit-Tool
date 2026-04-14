import re
from utils.llm_handler import query_llm


def analyze_response(p_name: str, p_key: str, response_text: str, client_name: str, country: str, model: str = None) -> dict:
    """
    Analyses an LLM response for sentiment, GEO score, and hallucination risk.
    Uses a structured prompt to minimise extra LLM calls cost.
    """
    prompt = f"""Analyze this LLM response about '{client_name}' in the {country} market.

Response: "{response_text[:1500]}"

Return ONLY in this exact format (no extra text):
Sentiment: <Positive|Neutral|Negative>
GEO Score: <1-10>
Hallucination Risk: <Low|Medium|High>
Entities: <comma-separated list of 2-3 key brands or topics mentioned>"""

    result = query_llm(p_name, p_key, prompt, model=model)
    raw = result.get("text", "")

    defaults = {
        "Sentiment": "Neutral",
        "GEO Score": "5",
        "Hallucination Risk": "Low",
        "Entities": "",
    }

    if result.get("error"):
        return defaults

    try:
        for line in raw.strip().splitlines():
            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                if key in defaults:
                    defaults[key] = val.strip()
    except Exception:
        pass

    # Normalise GEO score to integer string
    try:
        score = int(re.search(r"\d+", defaults["GEO Score"]).group())
        defaults["GEO Score"] = str(min(max(score, 1), 10))
    except Exception:
        defaults["GEO Score"] = "5"

    return defaults


def calculate_sov(response_text: str, client_name: str, competitors: list) -> dict:
    """
    Calculates Share of Voice as mention count (not just binary).
    Returns dict of {name: mention_count}.
    """
    text_lower = response_text.lower()
    mentions = {}

    def count_mentions(name: str) -> int:
        if not name:
            return 0
        return len(re.findall(r'\b' + re.escape(name.lower()) + r'\b', text_lower))

    mentions[client_name] = count_mentions(client_name)
    for comp in competitors:
        mentions[comp] = count_mentions(comp)

    return mentions
