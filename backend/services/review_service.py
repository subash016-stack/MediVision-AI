from database.connection import get_collection
from datetime import datetime
predictions = get_collection("predictions")
users = get_collection("users")


class ReviewService:

    @staticmethod
    def get_pending_predictions():

        prediction_list = list(
        predictions.find(
            {
                "doctor_status": "Pending"
            },
            {
                "_id": 0
            }
        ).sort("created_at", -1)
    )

        for prediction in prediction_list:

            patient = users.find_one(
                {
                    "user_id": prediction["user_id"]
                },
                {
                    "_id": 0,
                    "full_name": 1,
                    "email": 1
                }
            )

            if patient:

                prediction["patient_name"] = patient["full_name"]

                prediction["patient_email"] = patient["email"]

        return prediction_list
    @staticmethod
    def mark_reviewed(  
        prediction_id,
        review_data,
        current_user
    ):

        prediction = predictions.find_one(
            {
                "prediction_id": prediction_id
            }
        )

        if prediction is None:
            raise ValueError("Prediction not found.")

        predictions.update_one(
            {
                "prediction_id": prediction_id
            },
            {
                "$set": {

                    "doctor_status": "Reviewed",

                    "doctor_comments":
                        review_data.doctor_comments,

                    "reviewed_by":
                        current_user["user_id"],

                    "reviewed_at":
                        datetime.now()

                }
            }
        )
        return True