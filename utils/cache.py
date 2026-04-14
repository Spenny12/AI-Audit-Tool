"""
Feature 2 — Question-Level Result Caching (SQLite)
Caches each (question, provider, model) result to avoid re-spending API credits.
Cache key: SHA256 of (provider + model + prompt).
Results are stored indefinitely unless manually cleared.
"""
import hashlib
import json
import sqlite3
from pathlib import Path

CACHE_DB = Path("audit_cache.db")


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(CACHE_DB))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS response_cache (
            cache_key   TEXT PRIMARY KEY,
            provider    TEXT,
            model       TEXT,
            prompt_hash TEXT,
            result_json TEXT,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    return conn


def _make_key(provider: str, model: str, prompt: str) -> str:
    raw = f"{provider}|{model}|{prompt}"
    return hashlib.sha256(raw.encode()).hexdigest()


def get_cached(provider: str, model: str, prompt: str) -> dict | None:
    key = _make_key(provider, model, prompt)
    try:
        conn = _get_conn()
        row = conn.execute(
            "SELECT result_json FROM response_cache WHERE cache_key = ?", (key,)
        ).fetchone()
        conn.close()
        if row:
            return json.loads(row[0])
    except Exception:
        pass
    return None


def set_cached(provider: str, model: str, prompt: str, result: dict) -> None:
    key = _make_key(provider, model, prompt)
    try:
        conn = _get_conn()
        conn.execute(
            """INSERT OR REPLACE INTO response_cache
               (cache_key, provider, model, prompt_hash, result_json)
               VALUES (?, ?, ?, ?, ?)""",
            (key, provider, model, key[:16], json.dumps(result)),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def cache_stats() -> dict:
    """Returns total entries and DB file size."""
    try:
        conn = _get_conn()
        count = conn.execute("SELECT COUNT(*) FROM response_cache").fetchone()[0]
        conn.close()
        size_bytes = CACHE_DB.stat().st_size if CACHE_DB.exists() else 0
        return {"entries": count, "size_kb": round(size_bytes / 1024, 1)}
    except Exception:
        return {"entries": 0, "size_kb": 0}


def clear_cache() -> int:
    """Deletes all cached entries. Returns number of rows deleted."""
    try:
        conn = _get_conn()
        count = conn.execute("SELECT COUNT(*) FROM response_cache").fetchone()[0]
        conn.execute("DELETE FROM response_cache")
        conn.commit()
        conn.close()
        return count
    except Exception:
        return 0
