"""
LLM Handler — supports OpenAI, Google Gemini, and Perplexity.
Feature 6: Perplexity added (uses OpenAI-compatible API with sonar models).
Feature 12: Citation extraction — Perplexity returns citations natively;
            for OpenAI/Gemini we parse any URLs found in the response text.
"""
import re
import time
import openai
import google.generativeai as genai

# ── Available models per provider ────────────────────────────────────────────
OPENAI_MODELS = [
    "gpt-4o",
    "gpt-4-turbo",
    "gpt-4o-mini",
    "gpt-3.5-turbo",
]

GEMINI_MODELS = [
    "gemini-1.5-flash",
    "gemini-1.5-pro",
    "gemini-2.0-flash",
    "gemini-2.5-pro-preview-05-06",
]

PERPLEXITY_MODELS = [
    "sonar",
    "sonar-pro",
    "sonar-reasoning",
    "sonar-reasoning-pro",
]

PERPLEXITY_BASE_URL = "https://api.perplexity.ai"

# Regex to pull bare URLs out of plain text (for non-Perplexity providers)
_URL_RE = re.compile(r"https?://[^\s\)\]\"'<>]+")


def _extract_urls_from_text(text: str) -> list[str]:
    """Pull any URLs embedded in a plain-text response."""
    return list(dict.fromkeys(_URL_RE.findall(text)))  # deduplicated, order-preserved


def query_llm(
    provider: str,
    api_key: str,
    prompt: str,
    model: str | None = None,
    retries: int = 2,
) -> dict:
    """
    Query an LLM provider with retry logic.

    Returns a dict:
        text        : str   — the response text
        error       : str|None
        model       : str   — model that was actually used
        citations   : list  — list of URL strings cited in the response
        provider    : str
    """
    last_error = None

    for attempt in range(retries + 1):
        try:
            # ── OpenAI ────────────────────────────────────────────────────────
            if provider == "OpenAI":
                chosen_model = model or "gpt-4o"
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=chosen_model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30,
                )
                text = response.choices[0].message.content or ""
                return {
                    "text": text,
                    "error": None,
                    "model": chosen_model,
                    "citations": _extract_urls_from_text(text),
                    "provider": provider,
                }

            # ── Google Gemini ─────────────────────────────────────────────────
            elif provider == "Gemini":
                chosen_model = model or "gemini-1.5-flash"
                genai.configure(api_key=api_key)
                gmodel = genai.GenerativeModel(chosen_model)
                response = gmodel.generate_content(prompt)
                text = response.text or ""
                return {
                    "text": text,
                    "error": None,
                    "model": chosen_model,
                    "citations": _extract_urls_from_text(text),
                    "provider": provider,
                }

            # ── Perplexity (Feature 6 + 12) ───────────────────────────────────
            elif provider == "Perplexity":
                chosen_model = model or "sonar"
                client = openai.OpenAI(
                    api_key=api_key,
                    base_url=PERPLEXITY_BASE_URL,
                )
                response = client.chat.completions.create(
                    model=chosen_model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30,
                )
                text = response.choices[0].message.content or ""

                # Perplexity returns native citations in response metadata
                native_citations: list[str] = []
                try:
                    native_citations = list(response.citations) if hasattr(response, "citations") else []
                except Exception:
                    pass

                # Fallback: also parse URLs from the text itself
                text_citations = _extract_urls_from_text(text)
                all_citations = list(dict.fromkeys(native_citations + text_citations))

                return {
                    "text": text,
                    "error": None,
                    "model": chosen_model,
                    "citations": all_citations,
                    "provider": provider,
                }

        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))

    return {
        "text": "",
        "error": f"[{provider}] {last_error}",
        "model": model or "",
        "citations": [],
        "provider": provider,
    }
