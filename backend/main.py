from fastapi import FastAPI
from backend.api.endpoints import router  # Ensure correct import

app = FastAPI()

app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
