
from app.config import settings
from celery import Celery

#запускать через cmd


celery = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["app.back_tasks.tasks"]
)

