from ai_agents.crew import CrewAI


def analyze_sales_data():
    """Calls CrewAI to analyze sales and provide insights"""
    crew_instance = CrewAI()
    result = crew_instance.kickoff(inputs={"period": "monthly"})
    return {"insights": result}
