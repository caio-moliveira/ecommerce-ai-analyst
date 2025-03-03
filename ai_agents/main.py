from crew import CrewAI


def run():
    analysis = "What were the total sales last month?"
    crew_instance = CrewAI().set_analysis(analysis)
    crew_instance.crew().kickoff(inputs={"analysis": analysis})


if __name__ == "__main__":
    run()
