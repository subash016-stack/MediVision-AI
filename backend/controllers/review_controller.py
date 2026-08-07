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
    @staticmethod
    def review_prediction(
        prediction_id,
        review_data,
        current_user
    ):

        ReviewService.mark_reviewed(

            prediction_id,

            review_data,

            current_user

        )

        return ApiResponse.success(

            "Prediction reviewed successfully"

        )