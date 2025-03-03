from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
from ai_agents.tools.database_tool import fetch_sales_data


# Load YAML configurations
agents_config = "config/agents.yaml"
tasks_config = "config/tasks.yaml"


llm = LLM(model="ollama/deepseek-r1:8b", base_url="http://ollama:11434")


@CrewBase
class CrewAI:
    """Defines AI agents and tasks for data analysis."""

    def __init__(self):
        self.analysis = None

    def set_analysis(self, analysis):
        self.analysis = analysis
        return self

    @agent
    def data_agent(self) -> Agent:
        """E-commerce Data Assistant agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["data_assistant"],
            tools=[fetch_sales_data],
            verbose=True,
        )

    @agent
    def bi_agent(self) -> Agent:
        """Business Intelligence Analyst agent."""
        return Agent(
            llm=llm,
            config=self.agents_config["bi_analyst"],
            tools=[fetch_sales_data],
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
        )

    @task
    def report_task(self) -> Task:
        """Task to analyze business insights."""
        return Task(
            config=self.tasks_config["generate_report"],
            agent=self.bi_agent(),
            depends_on=[self.insights_task()],
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

    async def kickoff(self, inputs: dict):
        """Executes the AI analysis workflow."""
        try:
            return await self.crew().kickoff(inputs)
        except Exception as e:
            return {"error": str(e)}
