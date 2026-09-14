from datetime import datetime
import os

from database.connection import get_collection
from utils.prediction_id import generate_prediction_id
from ai.predictor import predict
from ai.model_loader import get_model
from ai.gradcam import generate_gradcam

images = get_collection("medical_images")
predictions = get_collection("predictions")
users = get_collection("users")


class PredictionService:

    @staticmethod
    def create_prediction(image_id, current_user):

        image = images.find_one({
            "image_id": image_id,
            "user_id": current_user["user_id"]
        },
        {
            "_id": 0
        }
        )

        if image is None:
            raise ValueError("Image not found.")

        result = predict(image["filepath"])

        count = predictions.count_documents({})
        prediction_id = generate_prediction_id(count)

        # Generate Grad-CAM Heatmap
        heatmap_rel_path = f"heatmaps/heatmap_{prediction_id}.png"
        try:
            model = get_model()
            generate_gradcam(model, image["filepath"], heatmap_rel_path)
            heatmap_url = heatmap_rel_path
        except Exception as e:
            print(f"Error generating Grad-CAM: {e}")
            heatmap_url = None

        prediction_document = {
            "prediction_id": prediction_id,
            "image_id": image_id,
            "user_id": current_user["user_id"],
            "disease": result["disease"],
            "confidence": result["confidence"],
            "heatmap_url": heatmap_url,

            # Doctor Review Fields
            "doctor_status": "Pending",
            "doctor_comments": "",
            "doctor_name": None,
            "reviewed_by": None,
            "reviewed_at": None,
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
            "heatmap_url": heatmap_url,
            "doctor_status": "Pending",
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
    def get_prediction_by_id(prediction_id, current_user):

        prediction = predictions.find_one(
            {
                "prediction_id": prediction_id
            },
            {
                "_id": 0
            }
        )

        if prediction is None:
            raise ValueError("Prediction not found.")

        # Ensure user is either the patient owner or a doctor
        if current_user.get("role") != "doctor" and prediction["user_id"] != current_user["user_id"]:
            raise ValueError("Unauthorized access to this prediction.")

        # Attach patient info
        patient = users.find_one(
            {
                "user_id": prediction["user_id"]
            },
            {
                "_id": 0,
                "full_name": 1,
                "email": 1,
                "phone": 1
            }
        )
        prediction["patient"] = patient

        # Attach image filepath
        image = images.find_one(
            {
                "image_id": prediction["image_id"]
            },
            {
                "_id": 0,
                "filepath": 1
            }
        )
        if image:
            prediction["image_url"] = image["filepath"]

        return prediction

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
