from datetime import datetime
from database.connection import db
from utils.security import hash_password


users_collection = db["users"]


def register_user(user):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if existing_user:
        return {
            "success": False,
            "message": "Email already registered"
        }

    new_user = {
        "full_name": user.full_name,
        "email": user.email,
        "phone": user.phone,
        "password": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.utcnow()
    }

    users_collection.insert_one(new_user)

    return {
        "success": True,
        "message": "Registration Successful"
    }