import smtplib
from email.message import EmailMessage
from crewai_tools import tool
import os

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")


@tool("send_email_report")
def send_email_report(to_email: str, subject: str, body: str) -> str:
    """Sends a report via email."""
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASS)
            smtp.send_message(msg)

        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {str(e)}"
