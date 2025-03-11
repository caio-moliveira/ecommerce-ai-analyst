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
        return CrewAI().crew().kickoff(inputs=inputs)
    except Exception as e:
        logger.error(f"❌ Error processing question: {e}", exc_info=True)
        return {"error": "An internal server error occurred."}
