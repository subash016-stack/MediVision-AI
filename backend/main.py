from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes.auth import router as auth_router
from routes.patient import router as patient_router
from routes.upload import router as upload_router
from routes.prediction import router as prediction_router
from routes.dashboard import router as dashboard_router

app = FastAPI(
    title="MediVision AI",
    version="1.0.0"
)

# ---------------- CORS ----------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- Routers ----------------

app.include_router(upload_router)
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(prediction_router)


app.include_router(dashboard_router)
# ---------------- Static Files ----------------

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