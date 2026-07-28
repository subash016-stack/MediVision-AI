from services.profile_service import ProfileService
from utils.response import ApiResponse


class ProfileController:

    @staticmethod
    def get_profile(current_user):

        try:

            result = ProfileService.get_profile(
                current_user
            )

            return ApiResponse.success(
                "Profile fetched successfully",
                result
            )

        except Exception as e:

            return ApiResponse.error(str(e))
    @staticmethod
    def update_profile(profile_data, current_user):

        try:

            ProfileService.update_profile(
                current_user,
                profile_data
            )

            return ApiResponse.success(
                "Profile updated successfully"
            )

        except Exception as e:

            return ApiResponse.error(str(e))
    @staticmethod
    def change_password(data, current_user):

        try:

            ProfileService.change_password(
                current_user,
                data
            )

            return ApiResponse.success(
                "Password changed successfully."
            )

        except Exception as e:

            return ApiResponse.error(str(e))