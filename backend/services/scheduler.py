from celery import Celery
from backend.services.report_generator import generate_report

celery = Celery("tasks", broker="redis://localhost:6379/0")


@celery.task
def schedule_report(period: str):
    """Runs scheduled sales reports"""
    generate_report(period)


celery.conf.beat_schedule = {
    "daily-report": {
        "task": "scheduler.schedule_report",
        "schedule": 86400.0,  # Every 24 hours
        "args": ("daily",),
    },
    "weekly-report": {
        "task": "scheduler.schedule_report",
        "schedule": 604800.0,  # Every week
        "args": ("weekly",),
    },
}
