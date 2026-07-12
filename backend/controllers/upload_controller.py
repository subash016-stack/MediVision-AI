from services.upload_service import UploadService
from utils.response import ApiResponse


class UploadController:

    @staticmethod
    def upload(file, current_user):

        try:

            result = UploadService.upload_image(
                file,
                current_user
            )

            return ApiResponse.success(
                "Image uploaded successfully",
                result
            )

        except Exception as e:

            return ApiResponse.error(str(e))
    @staticmethod
    def history(current_user):

        history = UploadService.get_history(
            current_user["user_id"]
        )

        return ApiResponse.success(
            "History fetched successfully",
            history
        )
    @staticmethod
    def delete(image_id, current_user):

        UploadService.delete_image(
            image_id,
            current_user["user_id"]
        )

        return ApiResponse.success(
            "Image deleted successfully"
        )