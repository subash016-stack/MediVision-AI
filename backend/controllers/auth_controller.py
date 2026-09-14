from fastapi import status

from services.auth_service import AuthService

from utils.response import ApiResponse


class AuthController:

    @staticmethod
    def login(user):

        success, result = AuthService.login(user)

        if not success:

            return ApiResponse.error(
                result,
                401
            )

        return ApiResponse.success(
            "Login Successful",
            result
        )
        
    @staticmethod
    def register(user):
        try:
            success, message = AuthService.register(user)

            if not success:
                return ApiResponse.error(
                    message,
                    status.HTTP_409_CONFLICT
                )

            return ApiResponse.success(
                message,
                status_code=status.HTTP_201_CREATED
            )
        except Exception as e:
            return ApiResponse.error(str(e), 500)

    @staticmethod
    def me(current_user):
        try:
            return ApiResponse.success(
                "Profile fetched successfully",
                current_user
            )
        except Exception as e:
            return ApiResponse.error(str(e), 500)