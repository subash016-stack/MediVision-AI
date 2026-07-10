from fastapi import status

from services.auth_service import AuthService
from utils.response import success, error


class AuthController:

    @staticmethod
    def register(user):

        ok, message = AuthService.register(user)

        if not ok:
            return error(
                message,
                status.HTTP_409_CONFLICT
            )

        return success(
            message,
            status_code=status.HTTP_201_CREATED
        )