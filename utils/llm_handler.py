import openai
import google.generativeai as genai
import time

OPENAI_MODELS = ["gpt-4o", "gpt-4-turbo", "gpt-4o-mini", "gpt-3.5-turbo"]
GEMINI_MODELS = ["gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash", "gemini-2.5-pro-preview-05-06"]

def query_llm(provider: str, api_key: str, prompt: str, model: str = None, retries: int = 2) -> dict:
    """
    Query an LLM provider with retry logic. Returns a dict with 'text' and 'error' keys.
    """
    last_error = None
    for attempt in range(retries + 1):
        try:
            if provider == "OpenAI":
                chosen_model = model or "gpt-4o"
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model=chosen_model,
                    messages=[{"role": "user", "content": prompt}],
                    timeout=30,
                )
                return {"text": response.choices[0].message.content, "error": None, "model": chosen_model}

            elif provider == "Gemini":
                chosen_model = model or "gemini-1.5-flash"
                genai.configure(api_key=api_key)
                gmodel = genai.GenerativeModel(chosen_model)
                response = gmodel.generate_content(prompt)
                return {"text": response.text, "error": None, "model": chosen_model}

        except Exception as e:
            last_error = str(e)
            if attempt < retries:
                time.sleep(1.5 * (attempt + 1))

    return {"text": "", "error": f"[{provider}] {last_error}", "model": model}
