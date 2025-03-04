from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
import logging
from backend.db.database import query_database_with_ai


llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://localhost:11434")

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
            tools=[query_database_with_ai],
            verbose=True,
        )

    @agent
    def bi_analyst(self) -> Agent:
        """Business Intelligence Analyst Agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["bi_analyst"],
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

    @crew
    def crew(self) -> Crew:
        """Runs the CrewAI execution process."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )

    def kickoff(self, question: str):
        """
        Executes the CrewAI workflow with the given question.
        """
        try:
            logger.info(f"🚀 Running CrewAI with question: {question}")

            # ✅ Ensure inputs is a dictionary
            result = self.crew().kickoff({"question": question})

            logger.info(f"✅ CrewAI Result: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ CrewAI Execution Failed: {e}", exc_info=True)
            return {"error": str(e)}
