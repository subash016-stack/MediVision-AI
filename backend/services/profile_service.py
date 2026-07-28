from database.connection import get_collection

users = get_collection("users")


class ProfileService:

    @staticmethod
    def get_profile(current_user):

        profile = users.find_one(
            {
                "user_id": current_user["user_id"]
            },
            {
                "_id": 0,
                "password": 0
            }
        )

        if profile is None:
            raise ValueError("User not found.")

        return profile