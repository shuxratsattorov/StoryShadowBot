from celery import Celery
from config.config import settings

celery_app = Celery(
    'insta_checker',
    broker=settings.REDIS_BROKER_URL,
    backend=settings.REDIS_BACKEND_URL,
    include=["tasks.check_stories"]
)


celery_app.conf.update(
    timezone='UTC',
    task_track_started=True,
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
)
