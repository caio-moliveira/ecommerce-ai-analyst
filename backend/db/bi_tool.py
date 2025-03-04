from crewai.tools import tool
from sqlalchemy import text
import logging
from backend.db.database import get_db

logger = logging.getLogger(__name__)


@tool("generate_insights")
async def generate_insights() -> str:
    """
    AI-driven BI analysis that generates a structured business intelligence report.

    :return: AI-generated insights including revenue, customer behavior, trends.
    """

    insights = {}
    queries = {
        "total_revenue": "SELECT SUM(total_value) FROM sales;",
        "average_order_value": "SELECT AVG(total_value) FROM sales;",
        "top_product": """
            SELECT product_name, SUM(quantity_sold) 
            FROM sales 
            GROUP BY product_name 
            ORDER BY SUM(quantity_sold) DESC 
            LIMIT 1;
        """,
        "top_customer": """
            SELECT customer_name, SUM(total_value) 
            FROM sales 
            GROUP BY customer_name 
            ORDER BY SUM(total_value) DESC 
            LIMIT 1;
        """,
        "top_region": """
            SELECT sales_region, SUM(total_value) 
            FROM sales 
            GROUP BY sales_region 
            ORDER BY SUM(total_value) DESC 
            LIMIT 1;
        """,
        "monthly_sales_trend": """
            SELECT DATE_TRUNC('month', sale_date) AS month, SUM(total_value) 
            FROM sales 
            GROUP BY month 
            ORDER BY month;
        """,
    }

    async for db in get_db():
        try:
            for key, query in queries.items():
                result = await db.execute(text(query))
                insights[key] = result.fetchall()
        except Exception as e:
            logger.error(f"❌ BI Analysis failed: {e}")
            return "Error generating insights."

    # Formatting the insights for AI agent response
    report = f"""
    🔥 **Business Intelligence Report**
    - **Total Revenue:** ${insights["total_revenue"][0][0]:,.2f}
    - **Avg Order Value:** ${insights["average_order_value"][0][0]:,.2f}
    - **Top-Selling Product:** {insights["top_product"][0][0]} ({insights["top_product"][0][1]} units sold)
    - **Top Customer:** {insights["top_customer"][0][0]} ($ {insights["top_customer"][0][1]:,.2f})
    - **Top Region:** {insights["top_region"][0][0]} ($ {insights["top_region"][0][1]:,.2f})

    📈 **Sales Trends**
    {insights["monthly_sales_trend"]}
    """
    return report
