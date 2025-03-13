from crew import CrewAI
from datetime import datetime


def run():
    """
    Run the crew.
    """
    inputs = {"topic": "Barcelona", "date": datetime.now().strftime("%Y-%m-%d")}
    CrewAI().crew().kickoff(inputs=inputs)


run()
