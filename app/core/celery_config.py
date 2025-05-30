from celery import Celery
from .settings import settings

celery_app = Celery(
    "fa_books",
    broker=settings.redis.redis_url,
    backend=settings.redis.redis_url,
    include=["app.api.v1.auth.tasks"],
)

celery_app.conf.task_routes = {
    "app.api.v1.auth.tasks.send_email_task": {"queue": "auth"},
}
