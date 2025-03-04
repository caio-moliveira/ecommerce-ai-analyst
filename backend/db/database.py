from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging
from crewai.tools import tool
from sqlalchemy.sql import text
import json


load_dotenv()

# ✅ Setup logging
logger = logging.getLogger(__name__)

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")


# Create a connection string
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
)

# Criar o motor assíncrono
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# Sessão assíncrona
async_session = sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)

# Base para os modelos declarativos
Base = declarative_base()


# Dependência para injeção de sessão no FastAPI
async def get_db():
    async with async_session() as session:
        yield session


# Inicializar o banco de dados
async def init_db():
    async with async_engine.begin() as conn:
        # Criar as tabelas (migrations podem substituir isso no futuro)
        await conn.run_sync(Base.metadata.create_all)


# ✅ Query Execution Tool
@tool("query_database_with_ai")
def query_database_with_ai(query: str) -> str:
    """
    Executes an AI-generated SQL query on the PostgreSQL database.

    Args:
        query (str): The SQL query string.

    Returns:
        str: JSON-formatted result set.
    """
    try:
        if not isinstance(query, str):
            raise ValueError("Query must be a string")

        db = next(get_db())
        result = db.execute(text(query))
        data = result.fetchall()

        response = [dict(row) for row in data]
        return json.dumps(response)

    except Exception as e:
        logger.error(f"❌ Database query error: {e}")
        return json.dumps({"error": str(e)})
