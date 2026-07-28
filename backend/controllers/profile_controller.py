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