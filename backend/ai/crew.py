from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase
import logging
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
import os
from dotenv import load_dotenv


load_dotenv()


# Load environment variables
DB_NAME = os.getenv("POSTGRES_DB")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# Initialize LLM
llm = LLM(model=OLLAMA_MODEL, base_url=OLLAMA_URL)

# Correct database connection
db_uri = f"postgresql://{DB_USER}:{DB_PASS}@postgresql:{DB_PORT}/{DB_NAME}"

# Initialize SQLDatabase (For executing queries)
sql_database = SQLDatabase.from_uri(db_uri)

# Initialize Query Tool (For executing SQL queries)
query_tool = QuerySQLDataBaseTool(db=sql_database)

logger = logging.getLogger(__name__)


@CrewBase
class CrewAI:
    """Defines AI agents and tasks for data analysis."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def data_assistant(self) -> Agent:
        """E-commerce Data Analyst Agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["data_assistant"],
            tools=[query_tool],
            verbose=True,
        )

    @task
    def sales_data(self) -> Task:
        """Task to fetch sales data from PostgreSQL."""
        return Task(
            config=self.tasks_config["sales_data"],
        )

    def crew1(self) -> Crew:
        """Creates the CrewaiFinAgent crew"""
        return Crew(
            agents=[self.data_assistant()],
            tasks=[self.sales_data()],
            process=Process.sequential,
            verbose=True,
        )
