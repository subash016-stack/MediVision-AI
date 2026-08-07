from services.doctor_service import DoctorService
from utils.response import ApiResponse


class DoctorController:

    @staticmethod
    def dashboard(current_user):

        data = DoctorService.dashboard(current_user)

        return ApiResponse.success(
            "Doctor dashboard loaded",
            data
        )