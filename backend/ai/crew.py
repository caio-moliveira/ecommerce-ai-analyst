from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
from backend.db.analyst_tool import query_database_with_ai
from backend.db.bi_tool import generate_insights


# Load YAML configurations
agents_config = "config/agents.yaml"
tasks_config = "config/tasks.yaml"


llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://ollama:11434")


@CrewBase
class CrewAI:
    """Defines AI agents and tasks for data analysis."""

    def __init__(self):
        self.agents_config = agents_config
        self.tasks_config = tasks_config

    @agent
    def data_agent(self) -> Agent:
        """E-commerce Data Analyst Agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["data_assistant"],
            tools=[query_database_with_ai],
            verbose=True,
        )

    @agent
    def bi_agent(self) -> Agent:
        """Business Intelligence Analyst Agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["bi_analyst"],
            tools=[generate_insights],
            verbose=True,
        )

    @task
    def fetch_sales_task(self) -> Task:
        """Task to fetch sales data from PostgreSQL."""
        return Task(
            config=self.tasks_config["sales_data"],
            agent=self.data_agent(),
        )

    @task
    def insights_task(self) -> Task:
        """Task to analyze business insights."""
        return Task(
            config=self.tasks_config["generate_insights"],
            agent=self.bi_agent(),
            depends_on=[
                self.fetch_sales_task()
            ],  # Ensure data is fetched before insights
        )

    @task
    def report_task(self) -> Task:
        """Task to generate a structured business report."""
        return Task(
            config=self.tasks_config["generate_report"],
            agent=self.bi_agent(),
            depends_on=[self.insights_task()],
        )

    @crew
    def crew(self) -> Crew:
        """Runs the CrewAI execution process."""
        return Crew(
            agents=[self.data_agent(), self.bi_agent()],
            tasks=[
                self.fetch_sales_task(),
                self.insights_task(),
                self.report_task(),
            ],  # Ensure tasks are defined
            process=Process.sequential,
            verbose=True,
        )

    async def kickoff(self, inputs: dict):
        """Executes the AI analysis workflow."""
        try:
            return await self.crew().kickoff(inputs)
        except Exception as e:
            return {"error": str(e)}
