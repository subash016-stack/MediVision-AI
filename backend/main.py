from fastapi import FastAPI
from database.connection import client
from routes.auth import router as auth_router

app = FastAPI(
    title="MediVision AI",
    version="1.0.0"
)

app.include_router(auth_router)

@app.get("/")
def home():
    return {
        "message": "Welcome to MediVision AI Backend"
    }


@app.get("/test-db")
def test_database():

    try:
        client.admin.command("ping")

        return {
            "status": "success",
            "message": "MongoDB Connected Successfully"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }