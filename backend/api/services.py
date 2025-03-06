import logging
from backend.ai.crew import CrewAI

logger = logging.getLogger(__name__)


def process_user_question(question: str) -> str:
    """
    Handles user queries and executes the Data Assistant.
    """
    try:
        logger.info(f"🔍 Processing user question: {question}")

        inputs = {"question": question}
        return CrewAI().crew1().kickoff(inputs=inputs)
    except Exception as e:
        logger.error(f"❌ Error processing question: {e}", exc_info=True)
        return {"error": "An internal server error occurred."}


def generate_report(period: str) -> str:
    """
    Handles report generation for a specific period using BI Analyst.
    """
    try:
        logger.info(f"📊 Generating business report for period: {period}")
        inputs = {"period": period}
        return CrewAI().crew2().kickoff(inputs=inputs)
    except Exception as e:
        logger.error(f"❌ Report generation failed: {e}", exc_info=True)
        return {"error": "Failed to generate report."}
