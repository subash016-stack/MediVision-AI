from database.connection import get_collection

users = get_collection("users")
predictions = get_collection("predictions")


class DoctorService:

    @staticmethod
    def dashboard_stats():

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

            "total_patients": total_patients,

            "total_predictions": total_predictions,

            "pending_reviews": pending_reviews,

            "completed_reviews": completed_reviews

        }