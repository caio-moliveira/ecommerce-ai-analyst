import uvicorn
from fastapi import FastAPI
from backend.api.routes import router as router
from backend.ai.crew import CrewAI

# Initialize FastAPI
app = FastAPI(title="AI-Powered Sales Analytics API", version="1.0")

# Register API routes
app.include_router(router)

# Initialize CrewAI
crew_ai = CrewAI()


@app.get("/")
async def root():
    """Root endpoint to check API health."""
    return {"message": "Welcome to the AI-powered Sales Analytics API!"}


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
