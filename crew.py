import os
from fastapi import FastAPI
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process, LLM
from crewai.project import agent, task, CrewBase, crew
from crewai_tools import SerperDevTool

app = FastAPI()

# Carregar as chaves da API
os.environ["OPENAI_API_KEY"] = "OPENAI_API_KEY"


llm = LLM(model="bedrock/anthropic.claude-3-sonnet-20240229-v1:0")


# Definir o modelo de entrada
class JobRequirements(BaseModel):
    job_requirements: str


@CrewBase
class CrewAI:
    """Defines AI agents and tasks for data analysis."""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[SerperDevTool()],
            verbose=True,
            memory=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config["research_task"],
            tools=[SerperDevTool()],
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[self.researcher()],
            tasks=[self.research_task()],
            process=Process.sequential,
            verbose=True,
        )


# Definir a rota para executar a tarefa
@app.post("/research_candidates")
async def research_candidates(req: JobRequirements):
    result = crew.kickoff(inputs={"job_requirements": req.job_requirements})
    return {"result": result}


# Rodar o servidor usando Uvicorn
if __name__ == "__main__":
    import uvicorn

    print(">>>>>>>>>>>> version V0.0.1")
    uvicorn.run(app, host="0.0.0.0", port=8000)
