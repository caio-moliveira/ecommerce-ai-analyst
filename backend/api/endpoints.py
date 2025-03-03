from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.services.ai_services import generate_ai_response
from backend.services.report_generator import generate_report
from pydantic import BaseModel

router = APIRouter()


class AnalysisRequest(BaseModel):
    question: str


@router.get("/sales")
async def get_sales_data(db: AsyncSession = Depends(get_db)):
    """Fetches sales data from the database"""
    try:
        async with db as session:
            sales = await session.execute("SELECT * FROM sales_data;")
            sales_result = sales.fetchall()
            if not sales_result:
                raise HTTPException(status_code=404, detail="No sales data found")
            return {"sales": sales_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ask")
async def ask_question(question: str):
    """
    Accepts a question from the user and generates an AI-driven response.
    """
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    response = await generate_ai_response(question)

    if "error" in response:
        raise HTTPException(status_code=500, detail=response["error"])

    return response


@router.post("/generate_report/{period}")
async def generate_sales_report(period: str):
    """Generates AI-driven sales report"""
    try:
        return generate_report(period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
