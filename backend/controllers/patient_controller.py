from services.patient_service import PatientService
from utils.response import ApiResponse


class PatientController:

    @staticmethod
    def profile(current_user):

        user = PatientService.get_profile(
            current_user["user_id"]
        )

        return ApiResponse.success(
            "Profile fetched successfully",
            user
        )