from fastapi import APIRouter
from backend.api.services import process_user_question
from backend.api.schemas import QuestionRequest

router = APIRouter()


@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Handles user questions and returns AI-generated responses.
    """
    response = process_user_question(request.question)
    return {"answer": response}
