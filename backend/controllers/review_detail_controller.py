from services.review_detail_service import ReviewDetailService
from utils.response import ApiResponse


class ReviewDetailController:

    @staticmethod
    def get_prediction(prediction_id):

        data = ReviewDetailService.get_prediction(
            prediction_id
        )

        return ApiResponse.success(
            "Prediction details fetched successfully",
            data
        )