from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.services.ai_analysis import analyze_sales_data
from backend.services.report_generator import generate_report

app = FastAPI()


@app.get("/sales")
async def get_sales_data(db: AsyncSession = Depends(get_db)):
    """Fetches sales data from the database"""
    try:
        result = await db.execute("SELECT * FROM sales")
        sales = result.fetchall()
        if not sales:
            raise HTTPException(status_code=404, detail="No sales data found")
        return sales
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_data():
    """Triggers AI analysis using CrewAI"""
    try:
        return await analyze_sales_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate_report/{period}")
async def generate_sales_report(period: str):
    """Generates and emails an AI-driven sales report"""
    try:
        return await generate_report(period)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
