from database.connection import get_collection

predictions = get_collection("predictions")
users = get_collection("users")
images = get_collection("medical_images")


class ReviewDetailService:

    @staticmethod
    def get_prediction(prediction_id):

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

        image = images.find_one(
            {
                "image_id": prediction["image_id"]
            },
            {
                "_id": 0,
                "filepath": 1
            }
        )

        prediction["patient"] = patient

        prediction["image_url"] = image["filepath"]

        return prediction