import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

settings = Settings()
