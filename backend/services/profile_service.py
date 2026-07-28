from database.connection import get_collection
from utils.security import verify_password, hash_password
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
    @staticmethod
    def update_profile(current_user, profile_data):

        result = users.update_one(
            {
                "user_id": current_user["user_id"]
            },
            {
                "$set": {
                    "full_name": profile_data.full_name,
                    "phone": profile_data.phone
                }
            }
        )

        if result.modified_count == 0:
            raise ValueError("No changes were made.")

        return True
    @staticmethod
    def change_password(current_user, data):

        user = users.find_one({
            "user_id": current_user["user_id"]
        })

        if not user:
            raise ValueError("User not found.")

        if not verify_password(
            data.current_password,
            user["password"]
        ):
            raise ValueError("Current password is incorrect.")

        users.update_one(
            {
                "user_id": current_user["user_id"]
            },
            {
                "$set": {
                    "password": hash_password(data.new_password)
                }
            }
        )

        return True