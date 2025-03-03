from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

# Obter as variáveis do arquivo .env
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")


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
        try:
            yield session
        finally:
            await session.close()


# Inicializar o banco de dados
async def init_db():
    async with async_engine.begin() as conn:
        # Criar as tabelas (migrations podem substituir isso no futuro)
        await conn.run_sync(Base.metadata.create_all)
