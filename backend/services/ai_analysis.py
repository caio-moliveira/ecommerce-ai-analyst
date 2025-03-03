from ai_agents.crew import CrewAI


async def analyze_sales_data(question: str):
    """Calls CrewAI to analyze sales and provide insights."""
    try:
        crew_instance = CrewAI().crew()
        result = await crew_instance.kickoff(
            inputs={"question": question}
        )  # ✅ Now kickoff works
        return {"insights": result}
    except Exception as e:
        return {"error": str(e)}
