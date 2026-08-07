from database.connection import get_collection

users = get_collection("users")
predictions = get_collection("predictions")


class DoctorService:

    @staticmethod
    def dashboard(current_user):
        total_patients = users.count_documents({
            "role": "patient"
        })

        total_predictions = predictions.count_documents({})

        pending_reviews = predictions.count_documents({
            "doctor_status": "Pending"
        })

        completed_reviews = predictions.count_documents({
            "doctor_status": "Reviewed"
        })

        return {

            "doctor": {

                "user_id": current_user["user_id"],
                "full_name": current_user["full_name"],
                "email": current_user["email"]

            },

            "stats": {

                "total_patients": total_patients,

                "total_predictions": total_predictions,

                "pending_reviews": pending_reviews,

                "completed_reviews": completed_reviews

            }

        }