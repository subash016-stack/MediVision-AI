from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

MODEL = tf.keras.models.load_model(
    os.getenv("MODEL_PATH")
)

class PredictionResponse(BaseModel):
    prediction_id: str
    disease: str
    confidence: float