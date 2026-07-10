from fastapi import APIRouter

from controllers.auth_controller import AuthController
from schemas.user import UserRegister

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/")
def auth_home():
    return {
        "message": "Authentication Module"
    }


@router.post("/register")
def register(user: UserRegister):
    return AuthController.register(user)