from pydantic import BaseModel


class PredictionResponse(BaseModel):
    prediction_id: str
    disease: str
    confidence: float