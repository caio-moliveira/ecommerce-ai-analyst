from celery.schedules import crontab

# Celery Configuration
timezone = "UTC"
result_backend = "redis://localhost:6379/0"

# Task execution limits
task_annotations = {
    "*": {"rate_limit": "10/s"}  # Max 10 tasks per second
}

# Periodic Task Schedule
beat_schedule = {
    "daily-report": {
        "task": "backend.scheduler.schedule_report",
        "schedule": crontab(hour=0, minute=0),  # Runs daily at midnight
        "args": ("daily",),
    },
    "weekly-report": {
        "task": "backend.scheduler.schedule_report",
        "schedule": crontab(day_of_week=1, hour=0, minute=0),  # Runs every Monday
        "args": ("weekly",),
    },
    "monthly-report": {
        "task": "backend.scheduler.schedule_report",
        "schedule": crontab(
            day_of_month=1, hour=0, minute=0
        ),  # Runs on the 1st of each month
        "args": ("monthly",),
    },
}
