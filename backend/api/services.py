import logging
from backend.ai.crew import CrewAI

logger = logging.getLogger(__name__)


def process_user_question(question: str):
    """
    Handles user queries and executes the Data Assistant.
    """
    try:
        logger.info(f"🔍 Processing user question: {question}")
        crew_instance = CrewAI()
        result = crew_instance.run_data_assistant(question)
        return {"answer": result}
    except Exception as e:
        logger.error(f"❌ Error processing question: {e}", exc_info=True)
        return {"error": "An internal server error occurred."}


def generate_report(period: str):
    """
    Handles report generation for a specific period using BI Analyst.
    """
    try:
        logger.info(f"📊 Generating business report for period: {period}")
        crew_instance = CrewAI()
        result = crew_instance.run_bi_analyst(period)
        return {"report": result}
    except Exception as e:
        logger.error(f"❌ Report generation failed: {e}", exc_info=True)
        return {"error": "Failed to generate report."}
