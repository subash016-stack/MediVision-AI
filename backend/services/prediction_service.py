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
    @staticmethod
    def get_prediction_history(current_user):

        history = list(
            predictions.find(
                {
                    "user_id": current_user["user_id"]
                },
                {
                    "_id": 0
                }
            ).sort("created_at", -1)
        )

        for item in history:

            image = images.find_one(
                {
                    "image_id": item["image_id"]
                },
                {
                    "_id": 0,
                    "filepath": 1
                }
            )

            if image:
                item["image_url"] = image["filepath"]

        return history
    @staticmethod
    def delete_prediction(prediction_id, current_user):

        prediction = predictions.find_one(
            {
                "prediction_id": prediction_id,
                "user_id": current_user["user_id"]
            }
        )

        if prediction is None:
            raise ValueError("Prediction not found.")

        predictions.delete_one(
            {
                "prediction_id": prediction_id
            }
        )

        return True
