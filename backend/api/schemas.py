from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Schema for AI question requests."""

    question: str  # Example: "What were the total sales last month?"


class AnswerResponse(BaseModel):
    """Schema for AI responses."""

    question: str
    answer: str  # AI-generated answer from the database.
