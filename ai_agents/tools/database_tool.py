from crewai.tools import tool
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@tool("fetch_sales_data")
def fetch_sales_data(query: str) -> str:
    """Fetches sales data from the PostgreSQL database based on a query."""
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DATABASE"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            port=os.getenv("POSTGRES_PORT"),
        )
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return str(result)
    except Exception as e:
        return f"Database query failed: {str(e)}"
