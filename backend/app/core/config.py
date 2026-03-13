import json
import os
from pathlib import Path

from dotenv import load_dotenv

# Load env files for local runs.
# Priority: existing process env vars > repo .env > backend/.env.
CURRENT_FILE = Path(__file__).resolve()
BACKEND_DIR = CURRENT_FILE.parents[2]
REPO_ROOT = CURRENT_FILE.parents[3]
load_dotenv(REPO_ROOT / ".env", override=False)
load_dotenv(BACKEND_DIR / ".env", override=False)

# Default total wait timeout for polling GET /runs/{id} (seconds). Clients/gateways should use at least this.
DEFAULT_RUN_POLL_TIMEOUT_SECONDS = 300


def _load_run_poll_timeout_from_settings_json() -> int | None:
    """Load run_poll_timeout_seconds from optional settings.json. Returns None if not found."""
    path = os.getenv("SETTINGS_PATH") or str(BACKEND_DIR / "settings.json")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        val = data.get("run_poll_timeout_seconds")
        if val is not None:
            return int(val)
    except (FileNotFoundError, json.JSONDecodeError, TypeError, ValueError):
        pass
    return None


class Settings:
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")

    # Total wait timeout for polling S18 GET /runs/{id}. Exposed via GET /health so clients/gateways can set their timeout.
    # Priority: env RUN_POLL_TIMEOUT_SECONDS > settings.json run_poll_timeout_seconds > env S18_POLL_TIMEOUT_SEC (backward compat) > default 300.
    @property
    def run_poll_timeout_seconds(self) -> int:
        env_val = os.getenv("RUN_POLL_TIMEOUT_SECONDS")
        if env_val is not None:
            try:
                return int(env_val)
            except (TypeError, ValueError):
                pass
        from_settings = _load_run_poll_timeout_from_settings_json()
        if from_settings is not None:
            return from_settings
        s18_val = os.getenv("S18_POLL_TIMEOUT_SEC")
        if s18_val is not None:
            try:
                return int(float(s18_val))
            except (TypeError, ValueError):
                pass
        return DEFAULT_RUN_POLL_TIMEOUT_SECONDS


settings = Settings()
