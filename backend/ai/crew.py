from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
import logging
from crewai_tools import PGSearchTool, NL2SQLTool
import os
from dotenv import load_dotenv

load_dotenv()


# Obter as variáveis do arquivo .env
DB_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")


llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://localhost:11434")

db_uri = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"

pgs_search_tool = PGSearchTool(db_uri=db_uri, table_name="public.sales")

nl2sql = NL2SQLTool(db_uri=db_uri)


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
            tools=[pgs_search_tool, nl2sql],
            verbose=True,
        )

    @agent
    def bi_analyst(self) -> Agent:
        """Business Intelligence Analyst Agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["bi_analyst"],
            tools=[pgs_search_tool, nl2sql],
            verbose=True,
        )

    @task
    def sales_data(self) -> Task:
        """Task to fetch sales data from PostgreSQL."""
        return Task(
            config=self.tasks_config["sales_data"],
        )

    @task
    def generate_insights(self) -> Task:
        """Task to analyze business insights."""
        return Task(
            config=self.tasks_config["generate_insights"],
        )

    @task
    def generate_report(self) -> Task:
        """Task to generate a structured business report."""
        return Task(
            config=self.tasks_config["generate_report"],
        )

    def run_data_assistant(self, question: str):
        """Executes only the data assistant agent."""
        try:
            logger.info(f"🟢 Running Data Assistant for question: {question}")
            crew = Crew(agents=[self.data_assistant()], tasks=[self.sales_data()])
            result = crew.kickoff({"question": question})
            return result
        except Exception as e:
            logger.error(f"❌ Data Assistant Execution Failed: {e}", exc_info=True)
            return {"error": str(e)}

    def run_bi_analyst(self, period: str):
        """Executes only the BI Analyst agent for insights & reports."""
        try:
            logger.info(f"🟢 Running BI Analyst for period: {period}")
            crew = Crew(
                agents=[self.bi_analyst()],
                tasks=[self.generate_insights(), self.generate_report()],
            )
            result = crew.kickoff({"period": period})
            return result
        except Exception as e:
            logger.error(f"❌ BI Analyst Execution Failed: {e}", exc_info=True)
            return {"error": str(e)}
