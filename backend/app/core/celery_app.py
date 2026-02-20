from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "wise_ai",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_BROKER_URL,
    include=["app.tasks.cbc_tasks"],
)
celery_app.conf.result_expires = 3600
