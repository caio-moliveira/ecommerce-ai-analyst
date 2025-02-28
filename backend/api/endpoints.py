from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.db.models import SalesData
from backend.services.ai_analysis import analyze_sales_data
from backend.services.report_generator import generate_report

app = FastAPI()


@app.get("/sales")
def get_sales_data(db: Session = Depends(get_db)):
    """Fetches sales data from the database"""
    return db.query(SalesData).all()


@app.post("/analyze")
def analyze_data():
    """Triggers AI analysis using CrewAI"""
    return analyze_sales_data()


@app.post("/generate_report/{period}")
def generate_sales_report(period: str):
    """Generates and emails an AI-driven sales report"""
    return generate_report(period)
