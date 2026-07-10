from fastapi import APIRouter
from schemas.user import UserRegister
from services.auth_service import register_user

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.get("/")
def auth_home():
    return {
        "message": "Authentication Route Working"
    }


@router.post("/register")
def register(user: UserRegister):

    result = register_user(user)

    return result