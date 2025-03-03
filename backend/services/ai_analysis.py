from ai_agents.crew import CrewAI


async def analyze_sales_data():
    """Calls CrewAI to analyze sales and provide insights."""
    try:
        crew_instance = CrewAI()
        result = await crew_instance.kickoff(inputs={"period": "monthly"})
        return {"insights": result}
    except Exception as e:
        return {"error": str(e)}
