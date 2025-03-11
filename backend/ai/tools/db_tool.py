from crewai.tools import tool
import os
import logging
from langchain_community.tools import QuerySQLDatabaseTool
from langchain_community.utilities.sql_database import SQLDatabase

logger = logging.getLogger(__name__)

# ✅ Load database environment variables
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")


# ✅ Function to get a fresh database connection
def get_sql_database():
    db_uri = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    try:
        return SQLDatabase.from_uri(db_uri)
    except Exception as e:
        logger.error(f"❌ Failed to connect to database: {e}", exc_info=True)
        raise


@tool
def query_database(query: str) -> str:
    """Executes an SQL query and returns structured results."""
    try:
        logger.info(f"Executing SQL query: {query}")
        with get_sql_database() as sql_database:
            query_tool = QuerySQLDatabaseTool(db=sql_database)
            result = query_tool.invoke(query)

        structured_response = {"query": query, "results": result}
        logger.info(f"Query Result: {structured_response}")
        return structured_response

    except Exception as e:
        logger.error(f"❌ SQL Execution Error: {e}", exc_info=True)
        return {"error": "Error executing SQL query."}
