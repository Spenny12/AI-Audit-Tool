import re
from utils.llm_handler import query_llm


def analyze_response(p_name: str, p_key: str, response_text: str, client_name: str, country: str, model: str = None) -> dict:
    """
    Analyses an LLM response for sentiment and hallucination risk.
    Uses a structured prompt to minimise extra LLM calls cost.
    """
    prompt = f"""Analyze this LLM response about '{client_name}' in the {country} market.

Response: "{response_text[:1500]}"

Return ONLY in this exact format (no extra text):
Sentiment: <Positive|Neutral|Negative>
Hallucination Risk: <Low|Medium|High>
Entities: <comma-separated list of 2-3 key brands or topics mentioned>"""

    result = query_llm(p_name, p_key, prompt, model=model)
    raw = result.get("text", "")

    defaults = {
        "Sentiment": "Neutral",
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
        # Use regex to find whole words, escaping name for safety
        pattern = r'\b' + re.escape(name.lower()) + r'\b'
        return len(re.findall(pattern, text_lower))

    mentions[client_name] = count_mentions(client_name)
    for comp in competitors:
        mentions[comp] = count_mentions(comp)

    return mentions


def calculate_geo_score(response_text: str, client_name: str, sentiment: str, sov: dict) -> str:
    """
    Calculates a deterministic GEO score (1-10) based on brand visibility.
    Factors: Presence, Sentiment, Position, and Share of Voice dominance.
    """
    if not client_name or client_name.lower() not in response_text.lower():
        return "1"

    score = 0
    text_lower = response_text.lower()
    client_lower = client_name.lower()

    # 1. Presence & Sentiment (Max 5)
    score += 3  # Base points for being mentioned
    sent = sentiment.lower()
    if sent == "positive":
        score += 2
    elif sent == "neutral":
        score += 1
    elif sent == "negative":
        score -= 1

    # 2. Position (Max 3)
    # Mentioned early (first 300 chars is roughly the first paragraph)
    if text_lower.find(client_lower) < 300:
        score += 2
    
    # Mentioned before any competitor
    first_comp_pos = 999999
    for name, count in sov.items():
        if name.lower() != client_lower and count > 0:
            pos = text_lower.find(name.lower())
            if pos != -1 and pos < first_comp_pos:
                first_comp_pos = pos
    
    if text_lower.find(client_lower) < first_comp_pos:
        score += 1

    # 3. Dominance (Max 2)
    client_mentions = sov.get(client_name, 0)
    max_comp_mentions = 0
    for name, count in sov.items():
        if name.lower() != client_lower:
            if count > max_comp_mentions:
                max_comp_mentions = count
    
    if client_mentions > max_comp_mentions:
        score += 2
    elif client_mentions == max_comp_mentions and client_mentions > 0:
        score += 1

    return str(min(max(score, 1), 10))
