from database.connection import get_collection

users = get_collection("users")


class PatientService:

    @staticmethod
    def get_profile(user_id):

        user = users.find_one(
            {
                "user_id": user_id
            },
            {
                "_id": 0,
                "password": 0
            }
        )

        return user