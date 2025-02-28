import pytest
from ai_agents.crew import CrewAI


@pytest.fixture
def crew_instance():
    """Initialize CrewAI instance for testing."""
    return CrewAI()


def test_agents_exist(crew_instance):
    """Test if agents are correctly initialized."""
    assert crew_instance.data_agent() is not None
    assert crew_instance.bi_agent() is not None


def test_tasks_exist(crew_instance):
    """Test if tasks are correctly initialized."""
    assert crew_instance.fetch_sales_task() is not None
    assert crew_instance.insights_task() is not None
    assert crew_instance.report_task() is not None


def test_crew_initialization(crew_instance):
    """Test if the Crew instance is correctly created."""
    crew = crew_instance.crew()
    assert crew is not None
    assert len(crew.agents) == 2  # Ensure both agents are loaded
    assert len(crew.tasks) == 3  # Ensure all tasks are included


def test_kickoff_execution(crew_instance):
    """Test if CrewAI kickoff runs without errors."""
    crew = crew_instance.crew()
    result = crew.kickoff(inputs={"period": "monthly"})
    assert result is not None
    assert isinstance(result, str)  # Ensure output is a valid string
