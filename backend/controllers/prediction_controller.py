from services.prediction_service import PredictionService
from utils.response import ApiResponse


class PredictionController:

    @staticmethod
    def predict(image_id, current_user):

        try:

            result = PredictionService.create_prediction(
                image_id,
                current_user
            )

            return ApiResponse.success(
                "Prediction completed successfully",
                result
            )

        except Exception as e:

            return ApiResponse.error(str(e))


    @staticmethod
    def history(current_user):

        try:

            result = PredictionService.get_prediction_history(
                current_user
            )

            return ApiResponse.success(
                "Prediction history fetched successfully",
                result
            )

        except Exception as e:

            return ApiResponse.error(str(e))


    @staticmethod
    def delete_prediction(
        prediction_id,
        current_user
    ):

        try:

            PredictionService.delete_prediction(
                prediction_id,
                current_user
            )

            return ApiResponse.success(
                "Prediction deleted successfully"
            )

        except Exception as e:

            return ApiResponse.error(str(e))