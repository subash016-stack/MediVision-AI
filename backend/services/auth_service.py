from datetime import datetime
from utils.id_generator import generate_user_id
from database.connection import get_collection
from utils.security import hash_password

from utils.security import (
    verify_password,
    create_access_token
)

users = get_collection("users")


class AuthService:

    @staticmethod  
    def login(user):

        existing = users.find_one(
            {
                "email": user.email
            }
        )


        if existing is None:
            return False, "Invalid Email"

        if not verify_password(
            user.password,
            existing["password"]
        ):
            return False, "Invalid Password"

        token = create_access_token(
            {
                "user_id": existing["user_id"],
                "email": existing["email"],
                "role": existing["role"]
            }
        )

        return True, {

            "access_token": token,

            "token_type": "Bearer",

            "user":{

                "user_id": existing["user_id"],

                "full_name": existing["full_name"],

                "email": existing["email"],

                "role": existing["role"]

            }

        }
    
    def register(user):

        existing = users.find_one(
            {
                "email": user.email
            }
        )

        if existing:
            return False, "Email already exists"

        count = users.count_documents({})
        user_id = generate_user_id(count)

        new_user = {

        "user_id": user_id,

        "full_name": user.full_name,

        "email": user.email,

        "phone": user.phone,

        "password": hash_password(user.password),

        "role": user.role,

        "created_at": datetime.now()

    }

        users.insert_one(new_user)

        return True, "Registration Successful"