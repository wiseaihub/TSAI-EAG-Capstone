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


class Settings:
    DATABASE_URL: str | None = os.getenv("DATABASE_URL")


settings = Settings()
