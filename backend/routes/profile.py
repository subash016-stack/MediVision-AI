from fastapi import APIRouter, Depends

from controllers.profile_controller import ProfileController
from middleware.auth_middleware import get_current_user

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.get("/me")
def get_profile(
    current_user=Depends(get_current_user)
):

    return ProfileController.get_profile(
        current_user
    )