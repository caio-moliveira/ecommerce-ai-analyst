import logging
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.analyst_tool import query_database_with_ai
from backend.db.bi_tool import generate_insights

logger = logging.getLogger(__name__)


async def process_user_question(question: str, db: AsyncSession) -> str:
    """
    Handles a user's question by dynamically querying the sales database.

    - Calls `query_database_with_ai()` from analyst_tool.py.
    - Returns a structured AI response.

    :param question: User's question about sales data.
    :param db: Async database session.
    :return: AI-generated response with relevant data.
    """
    try:
        logger.info(f"📊 Processing user question: {question}")
        response = await query_database_with_ai(question)
        return response
    except Exception as e:
        logger.error(f"❌ Error processing question: {e}")
        return "Error processing your request."


async def generate_report(db: AsyncSession) -> str:
    """
    Generates a full business intelligence report using AI-driven insights.

    - Calls `generate_insights()` from bi_tool.py.
    - Returns structured data analysis.

    :param db: Async database session.
    :return: AI-generated structured report.
    """
    try:
        logger.info("📈 Generating Business Intelligence Report...")
        report = await generate_insights()
        return report
    except Exception as e:
        logger.error(f"❌ Error generating BI report: {e}")
        return "Error generating business insights."
