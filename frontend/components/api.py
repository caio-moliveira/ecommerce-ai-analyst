import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


def fetch_sales_data():
    """Fetches sales data from the backend API."""
    response = requests.get(f"{BACKEND_URL}/sales")
    return response.json() if response.status_code == 200 else None


def analyze_data(question: str):
    """Sends a question to CrewAI for analysis."""
    response = requests.post(f"{BACKEND_URL}/analyze", json={"question": question})
    return response.json() if response.status_code == 200 else None


def generate_report(period: str):
    """Requests AI-generated sales report."""
    response = requests.post(f"{BACKEND_URL}/generate_report/{period}")
    return response.json() if response.status_code == 200 else None
