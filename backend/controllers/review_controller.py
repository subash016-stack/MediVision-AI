from services.review_service import ReviewService
from utils.response import ApiResponse


class ReviewController:

    @staticmethod
    def get_pending():

        data = ReviewService.get_pending_predictions()

        return ApiResponse.success(
            "Predictions fetched successfully",
            data
        )