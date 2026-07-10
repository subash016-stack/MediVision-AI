from fastapi import FastAPI

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