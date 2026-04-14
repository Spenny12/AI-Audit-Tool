"""
Feature 1 — Saved Audit Profiles
Stores client configurations as named JSON files in a local ./profiles/ directory.
Each profile contains: name, website, industry, service, competitors, country,
and optionally the chosen models.
"""
import json
import os
from pathlib import Path

PROFILES_DIR = Path("profiles")


def _ensure_dir():
    PROFILES_DIR.mkdir(exist_ok=True)


def list_profiles() -> list[str]:
    _ensure_dir()
    return sorted(p.stem for p in PROFILES_DIR.glob("*.json"))


def save_profile(name: str, data: dict) -> None:
    _ensure_dir()
    safe_name = "".join(c if c.isalnum() or c in "._- " else "_" for c in name).strip()
    path = PROFILES_DIR / f"{safe_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def load_profile(name: str) -> dict | None:
    _ensure_dir()
    path = PROFILES_DIR / f"{name}.json"
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def delete_profile(name: str) -> bool:
    path = PROFILES_DIR / f"{name}.json"
    if path.exists():
        path.unlink()
        return True
    return False


def profile_to_dict(
    client_name: str,
    website_url: str,
    industry: str,
    core_service: str,
    competitors: list,
    country: str,
    openai_model: str = "",
    gemini_model: str = "",
    perplexity_model: str = "",
) -> dict:
    return {
        "client_name": client_name,
        "website_url": website_url,
        "industry": industry,
        "core_service": core_service,
        "competitors": competitors,
        "country": country,
        "openai_model": openai_model,
        "gemini_model": gemini_model,
        "perplexity_model": perplexity_model,
    }
