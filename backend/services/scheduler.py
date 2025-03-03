from celery import Celery
from backend.services.report_generator import generate_report
import logging

# Initialize Celery
celery = Celery("tasks", broker="redis://localhost:6379/0")

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@celery.task
def schedule_report(period: str):
    """Runs scheduled AI-generated sales reports."""
    try:
        logging.info(f"📊 Generating {period} sales report...")
        result = generate_report(period)
        logging.info(f"✅ Report generated successfully: {result}")
        return result
    except Exception as e:
        logging.error(f"❌ Error generating {period} report: {str(e)}")
        return {"error": str(e)}


# Load Celery config
celery.config_from_object("backend.scheduler.celeryconfig")
