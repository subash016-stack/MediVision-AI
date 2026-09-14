from fastapi import APIRouter, Depends

from controllers.prediction_controller import PredictionController
from middleware.role_middleware import require_patient
from middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/prediction",
    tags=["Prediction"]
)


@router.post("/{image_id}")
def predict(
    image_id: str,
    current_user=Depends(require_patient)
):
    return PredictionController.predict(
        image_id,
        current_user
    )


@router.get("/history")
def history(
    current_user=Depends(require_patient)
):
    return PredictionController.history(
        current_user
    )


@router.get("/details/{prediction_id}")
def prediction_details(
    prediction_id: str,
    current_user=Depends(get_current_user)
):
    return PredictionController.get_prediction_details(
        prediction_id,
        current_user
    )


@router.delete("/{prediction_id}")
def delete_prediction(
    prediction_id: str,
    current_user=Depends(require_patient)
):
    return PredictionController.delete_prediction(
        prediction_id,
        current_user
    )