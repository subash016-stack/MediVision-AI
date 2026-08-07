from fastapi import APIRouter, Depends

from controllers.doctor_controller import DoctorController
from middleware.role_middleware import require_doctor

router = APIRouter(
    prefix="/doctor",
    tags=["Doctor"]
)

@router.get("/dashboard")
def dashboard(
    current_user=Depends(require_doctor)
):
    return DoctorController.dashboard(current_user)