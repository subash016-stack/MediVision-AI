from datetime import datetime

from database.connection import db
from utils.security import hash_password

users = db["users"]


class AuthService:

    @staticmethod
    def register(user):

        existing = users.find_one({"email": user.email})

        if existing:
            return False, "Email already registered"

        new_user = {
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "password": hash_password(user.password),
            "role": user.role,
            "created_at": datetime.utcnow()
        }

        users.insert_one(new_user)

        return True, "Registration Successful"