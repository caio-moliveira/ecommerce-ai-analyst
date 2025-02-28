import pandas as pd
from backend.db.database import get_db
from backend.db.models import SalesData
from ai_agents.tools.email_tool import send_email_report


def generate_report(period: str):
    """Generates a sales report and sends it via email"""
    db = next(get_db())
    sales_data = db.query(SalesData).all()

    # Convert sales data to Pandas DataFrame
    df = pd.DataFrame([s.__dict__ for s in sales_data])

    # Generate CSV file
    file_path = f"reports/sales_report_{period}.csv"
    df.to_csv(file_path, index=False)

    # Send report via email
    send_email_report(
        "client@example.com",
        f"{period.capitalize()} Sales Report",
        f"Attached is your {period} sales report.",
        file_path,
    )

    return {"message": f"{period.capitalize()} sales report generated and emailed!"}
