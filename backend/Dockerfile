# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy backend and AI agents
COPY backend/ ./backend
COPY ai_agents/ ./ai_agents

# Set the Python path to include the app directory
ENV PYTHONPATH=/app

# Install dependencies
RUN pip install --no-cache-dir -r backend/requirements.txt

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI properly
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
