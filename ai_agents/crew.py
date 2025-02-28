from crewai import Agent, Task, Crew, Process
from crewai.project import agent, task, crew, CrewBase
from crewai_tools import SerperDevTool


@CrewBase
class CrewAI:
    """Main class to define CrewAI agents, tasks, and execution process."""

    # Load agents and tasks from YAML
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def data_agent(self) -> Agent:
        """Defines the E-commerce Data Assistant agent."""
        return Agent(
            config=self.agents_config["data_assistant"],
            tools=[SerperDevTool()],
            verbose=True,
            memory=False,
        )

    @agent
    def bi_agent(self) -> Agent:
        """Defines the Business Intelligence Analyst agent."""
        return Agent(
            config=self.agents_config["bi_analyst"],
            tools=[SerperDevTool()],
            verbose=True,
            memory=False,
        )

    @task
    def fetch_sales_task(self) -> Task:
        """Defines the task to fetch sales data from PostgreSQL."""
        return Task(
            config=self.tasks_config["fetch_sales_data"],
            agent=self.data_agent(),
        )

    @task
    def insights_task(self) -> Task:
        """Defines the task to analyze business insights."""
        return Task(
            config=self.tasks_config["generate_insights"],
            agent=self.bi_agent(),
        )

    @task
    def report_task(self) -> Task:
        """Defines the task to generate automated reports."""
        return Task(
            config=self.tasks_config["generate_report"],
            agent=self.data_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Defines the CrewAI execution process."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            processes=Process.sequential,
            verbose=True,
        )
