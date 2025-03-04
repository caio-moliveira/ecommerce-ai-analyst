from pydantic import BaseModel


class QuestionRequest(BaseModel):
    """Schema for AI question requests."""

    question: str  # Example: "What were the total sales last month?"


class AnswerResponse(BaseModel):
    """Schema for AI responses."""

    question: str
    answer: str  # AI-generated answer from the database.


class ReportRequest(BaseModel):
    """Schema for AI-generated reports."""

    report_type: str  # Example: "monthly_sales", "customer_behavior"


class ReportResponse(BaseModel):
    """Schema for BI report responses."""

    report_type: str
    report: str  # AI-generated insights & graphs.
