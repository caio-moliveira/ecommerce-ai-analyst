from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import (
    QuestionRequest,
    AnswerResponse,
    ReportRequest,
    ReportResponse,
)
from services import process_user_question, generate_report
from db.database import get_db

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/ask", response_model=AnswerResponse)
async def ask_ai(request: QuestionRequest, db: Session = Depends(get_db)):
    """
    Users ask the AI a question about sales data.
    The AI (Data Analyst Agent) retrieves the answer from the database.
    """
    answer = process_user_question(request.question, db)
    return {"question": request.question, "answer": answer}


@router.post("/report", response_model=ReportResponse)
async def get_report(request: ReportRequest, db: Session = Depends(get_db)):
    """
    Users request a sales/business intelligence report.
    The AI (BI Analyst Agent) analyzes sales trends & generates insights.
    """
    report = generate_report(request.report_type, db)
    return {"report_type": request.report_type, "report": report}
