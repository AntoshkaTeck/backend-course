from celery import Celery

from src.config import settings

celery_instance = Celery(
    "tasks",
    broker=settings.REDIS_URL,
    include=["src.tasks.tasks"],
)

celery_instance.conf.beat_schedule = {
    # Ключ - любое название
    "0": {
        "task": "booking_today_checkin",  # Название таски, в которое в декораторе
        "schedule": 5,  # секунды (если сложно: crontab(minute=...))
    }
}
