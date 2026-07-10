from fastapi import APIRouter

from schemas.user import UserRegister

from controllers.auth_controller import AuthController

from schemas.user import UserLogin

from middleware.auth_middleware import get_current_user
from fastapi import Depends

from middleware.role_middleware import (
    require_patient,
    require_doctor,
    require_admin
)
from fastapi import Depends

router = APIRouter(

    prefix="/auth",

    tags=["Authentication"]

)


@router.get("/")
def auth_home():

    return {

        "message": "Authentication Module"

    }

@router.post("/login")
def login(user: UserLogin):

    return AuthController.login(user)


@router.post("/register")
def register(user: UserRegister):

    return AuthController.register(user)

@router.get("/me")
def get_profile(
    current_user=Depends(get_current_user)
):

    return {
        "success": True,
        "data": current_user
    }

@router.get("/patient/dashboard")
def patient_dashboard(
    current_user=Depends(require_patient)
):
    return {
        "message": "Welcome Patient",
        "user": current_user
    }

@router.get("/doctor/dashboard")
def doctor_dashboard(
    current_user=Depends(require_doctor)
):
    return {
        "message": "Welcome Doctor",
        "user": current_user
    }

@router.get("/admin/dashboard")
def admin_dashboard(
    current_user=Depends(require_admin)
):
    return {
        "message": "Welcome Admin",
        "user": current_user
    }

