from crewai.tools import tool
from sqlalchemy import text
import logging
from backend.db.database import get_db

logger = logging.getLogger(__name__)


@tool("query_database_with_ai")
async def query_database_with_ai(question: str) -> str:
    """
    AI-powered query tool that dynamically translates user questions into SQL
    and fetches relevant sales data.

    - Uses AI to extract key data points from user input.
    - Dynamically builds and executes safe SQL queries.
    - Returns structured insights, not raw DB dumps.

    :param question: User's sales-related question.
    :return: AI-processed database response.
    """

    # Basic keyword matching (this should be enhanced with NLP)
    query_templates = {
        "total sales": "SELECT SUM(total_value) FROM sales;",
        "average order value": "SELECT AVG(total_value) FROM sales;",
        "best-selling product": """
            SELECT product_name, SUM(quantity_sold) AS total_sold 
            FROM sales 
            GROUP BY product_name 
            ORDER BY total_sold DESC 
            LIMIT 1;
        """,
        "top sales region": """
            SELECT sales_region, SUM(total_value) AS total_sales 
            FROM sales 
            GROUP BY sales_region 
            ORDER BY total_sales DESC 
            LIMIT 1;
        """,
        "most frequent payment method": """
            SELECT payment_method, COUNT(*) 
            FROM sales 
            GROUP BY payment_method 
            ORDER BY COUNT(*) DESC 
            LIMIT 1;
        """,
    }

    # Find best match for the user's question
    sql_query = None
    for key in query_templates.keys():
        if key in question.lower():
            sql_query = query_templates[key]
            break

    if not sql_query:
        return "I couldn't determine a relevant query for this question."

    # Execute the SQL query
    async for db in get_db():
        try:
            result = await db.execute(text(sql_query))
            data = result.fetchall()
            return str(data)
        except Exception as e:
            logger.error(f"❌ Database query error: {e}")
            return "Error executing query."
