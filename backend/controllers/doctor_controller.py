from services.doctor_service import DoctorService
from utils.response import ApiResponse


class DoctorController:

    @staticmethod
    def dashboard():

        data = DoctorService.dashboard_stats()

        return ApiResponse.success(

            "Doctor dashboard loaded",

            data

        )