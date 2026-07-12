from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ApiResponse:

    @staticmethod
    def success(message, data=None, status_code=200):

        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder({
                "success": True,
                "message": message,
                "data": data
            })
        )

    @staticmethod
    def error(message, status_code=400):

        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message
            }
        )