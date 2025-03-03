# Use official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the backend folder and the ai_agents folder
COPY backend /app/backend
COPY ai_agents /app/ai_agents

# Install dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Set the PYTHONPATH so FastAPI can find backend as a module
ENV PYTHONPATH=/app

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
