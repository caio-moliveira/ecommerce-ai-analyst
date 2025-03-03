from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.services.ai_analysis import analyze_sales_data
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


@router.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    """Runs AI analysis synchronously (no Celery)"""
    try:
        return await analyze_sales_data(request.question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate_report/{period}")
async def generate_sales_report(period: str):
    """Generates AI-driven sales report"""
    try:
        return generate_report(period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
