from ai_agents.crew import CrewAI


async def generate_ai_response(question: str):
    """Calls AI agents (CrewAI) to generate a response for the given question."""
    try:
        crew_instance = CrewAI()
        response = await crew_instance.kickoff(
            inputs={"question": question}
        )  # ✅ Calls `kickoff()`
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}
