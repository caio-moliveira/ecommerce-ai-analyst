from fastapi import FastAPI
from backend.api.endpoints import router

app = FastAPI()

# ✅ Register API Routes
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "Backend is running!"}
