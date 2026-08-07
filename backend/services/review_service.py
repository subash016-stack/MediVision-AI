from database.connection import get_collection

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