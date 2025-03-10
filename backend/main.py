import uvicorn
from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="AI-Powered Sales Analytics API", version="1.0")

app.include_router(router)


@app.get("/")
async def root():
    """Root endpoint to check API health."""
    return {"message": "Welcome to the AI-powered Sales Analytics API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
