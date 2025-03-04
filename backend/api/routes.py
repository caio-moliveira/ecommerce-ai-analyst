from fastapi import APIRouter
from backend.api.services import process_user_question, generate_report

router = APIRouter()


@router.post("/ai/ask")
def ask_question(question: str):
    """
    API endpoint to receive user questions and trigger AI execution.
    """
    response = process_user_question(question)
    return response


@router.post("/ai/report")
def generate_ai_report():
    """
    API endpoint to trigger AI report generation separately.
    """
    response = generate_report()
    return response
