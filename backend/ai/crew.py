from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
import logging
from backend.ai.tools.db_tool import query_database


# Initialize LLM
llm = LLM(model="llama3.3:latest", base_url="http://0.0.0.0:11434")


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
            config=self.agents_config["data_assistant"],
            tools=[query_database],
            verbose=True,
        )

    @task
    def sales_data(self) -> Task:
        """Task to fetch sales data from PostgreSQL."""
        return Task(
            config=self.tasks_config["sales_data"],
            tools=[query_database],
            expected_output="A JSON object with SQL query and results.",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiFinAgent crew"""
        return Crew(
            agents=[self.data_assistant()],
            tasks=[self.sales_data()],
            process=Process.sequential,
            verbose=True,
        )
