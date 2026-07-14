from datetime import datetime

from database.connection import get_collection

from utils.prediction_id import generate_prediction_id
from ai.predictor import predict

images = get_collection("medical_images")
predictions = get_collection("predictions")


class PredictionService:

    @staticmethod
    def create_prediction(image_id, current_user):

        image = images.find_one({
            "image_id": image_id,
            "user_id": current_user["user_id"]
        },
        {
            "_id":0
        }
        )

        if image is None:
            raise ValueError("Image not found.")

        result = predict(image["filepath"])

        count = predictions.count_documents({})

        prediction_id = generate_prediction_id(count)

        prediction_document = {

            "prediction_id": prediction_id,

            "image_id": image_id,

            "user_id": current_user["user_id"],

            "disease": result["disease"],

            "confidence": result["confidence"],



            "created_at": datetime.now()

        }

        predictions.insert_one(prediction_document)

        images.update_one(
            {
                "image_id": image_id
            },
            {
                "$set": {
                    "prediction_status": "Completed"
                }
            }
        )
        
        return {
    "prediction_id": prediction_id,

    "image_id": image_id,

    "user_id": current_user["user_id"],

    "disease": result["disease"],

    "confidence": result["confidence"],

  

    "created_at": prediction_document["created_at"]
}

