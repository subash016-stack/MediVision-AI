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