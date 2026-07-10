from fastapi import APIRouter

from schemas.user import UserRegister

from controllers.auth_controller import AuthController

from schemas.user import UserLogin

from middleware.auth_middleware import get_current_user

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
def current_user(user=Depends(get_current_user)):
    return {
        "success": True,
        "user": user
    }