from fastapi import APIRouter, Depends

from middleware.role_middleware import require_patient
from controllers.patient_controller import PatientController

router = APIRouter(
    prefix="/patient",
    tags=["Patient"]
)


@router.get("/profile")
def profile(
    current_user=Depends(require_patient)
):
    return PatientController.profile(current_user)