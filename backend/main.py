from fastapi import FastAPI

from routes.auth import router as auth_router

from routes.patient import router as patient_router

app = FastAPI(

    title="MediVision AI",

    version="1.0.0"

)


app.include_router(auth_router)

app.include_router(patient_router)


@app.get("/")
def home():

    return {

        "message": "Welcome to MediVision AI Backend"

    }