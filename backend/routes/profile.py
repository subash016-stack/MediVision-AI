from fastapi import APIRouter, Depends
from schemas.change_password import ChangePassword
from controllers.profile_controller import ProfileController
from middleware.auth_middleware import get_current_user
from schemas.profile import UpdateProfile
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
@router.put("/update")
def update_profile(
    profile_data: UpdateProfile,
    current_user=Depends(get_current_user)
):

    return ProfileController.update_profile(
        profile_data,
        current_user
    )
@router.put("/change-password")
def change_password(
    data: ChangePassword,
    current_user=Depends(get_current_user)
):

    return ProfileController.change_password(
        data,
        current_user
    )