import logging
from backend.ai.crew import CrewAI

logger = logging.getLogger(__name__)
crew_ai = CrewAI()


def process_user_question(question: str):
    """
    Handles user queries and executes AI analysis.
    """
    try:
        logger.info(f"🔍 Processing user question: {question}")
        result = crew_ai.kickoff({"question": question})

        if isinstance(result, dict) and "error" in result:
            return {"error": "Failed to process request."}

        return {"answer": result}

    except Exception as e:
        logger.error(f"❌ Error processing question: {e}", exc_info=True)
        return {"error": "An internal server error occurred."}


def generate_report():
    """
    Triggers only the report generation task.
    """
    try:
        logger.info("📊 Generating business report...")
        result = crew_ai.kickoff({"generate_report": True})  # Run report task only
        return {"report": result}
    except Exception as e:
        logger.error(f"❌ Report generation failed: {e}", exc_info=True)
        return {"error": "Failed to generate report."}
