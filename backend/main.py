from fastapi import FastAPI

from routes.auth import router as auth_router

from routes.patient import router as patient_router

from fastapi.staticfiles import StaticFiles

from routes.upload import router as upload_router

from routes.prediction import router as prediction_router


app = FastAPI(

    title="MediVision AI",

    version="1.0.0"

)



app.include_router(upload_router)

app.include_router(auth_router)

app.include_router(patient_router)

app.include_router(prediction_router)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads"
)


@app.get("/")
def home():

    return {

        "message": "Welcome to MediVision AI Backend"

    }