import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def load_env():
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8-sig").splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.removeprefix("export ").split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip("'\""))


load_env()


def role(name):
    up = name.upper()
    return {
        "base_url": os.environ.get(f"{up}_BASE_URL") or os.environ.get("LLM_BASE_URL", "https://openrouter.ai/api/v1"),
        "api_key": os.environ.get(f"{up}_API_KEY") or os.environ.get("LLM_API_KEY", ""),
        "model": os.environ[f"{up}_MODEL"],
        "effort": os.environ.get(f"{up}_EFFORT"),
    }


# Domains the referee reads; searchers never see results from them.
REFEREE_DOMAINS = ["wikidata.org"]

# Per-attempt Telem spend cap in dollars. Cheaper routing buys more searches.
ATTEMPT_BUDGET = float(os.environ.get("ATTEMPT_BUDGET", "0.08"))
