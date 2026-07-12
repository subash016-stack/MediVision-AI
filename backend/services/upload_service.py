import os
import shutil
from datetime import datetime
from PIL import Image
import os
from database.connection import get_collection
from utils.image_id import generate_image_id

images = get_collection("medical_images")


class UploadService:

    @staticmethod
    def upload_image(file, current_user):

        # Count existing images
        count = images.count_documents({})

        # Generate image ID
        image_id = generate_image_id(count)

        # Get file extension
        extension = file.filename.split(".")[-1].lower()

        # Validate extension
        allowed_extensions = ["png", "jpg", "jpeg"]

        if extension not in allowed_extensions:
            raise ValueError(
                "Only PNG, JPG and JPEG images are allowed."
            )

        # ✅ Verify image using Pillow (ADD HERE)
        try:
            image = Image.open(file.file)
            image.verify()

            # Reset pointer because verify() reads the file
            file.file.seek(0)

        except Exception:
            raise ValueError("Invalid image file.")

        # Create new filename
        filename = f"{image_id}.{extension}"

        # File path
        filepath = os.path.join(
            "uploads",
            "xrays",
            filename
        )

        # Save image
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # MongoDB document
        image_document = {
            "image_id": image_id,
            "user_id": current_user["user_id"],
            "filename": filename,
            "filepath": filepath,
            "prediction_status": "Pending",
            "uploaded_at": datetime.now()
        }

        images.insert_one(image_document)

        return {
            "image_id": image_id,
            "image_url": "/" + filepath.replace("\\", "/")
        }
    @staticmethod
    def get_history(user_id):

        history = list(
            images.find(
                {
                    "user_id": user_id
                },
                {
                    "_id": 0
                }
            ).sort("uploaded_at", -1)
        )

        return history
    @staticmethod
    def delete_image(image_id, user_id):

        image = images.find_one({
            "image_id": image_id,
            "user_id": user_id
        })

        if image is None:
            raise ValueError("Image not found.")

        if os.path.exists(image["filepath"]):
            os.remove(image["filepath"])

        images.delete_one({
            "image_id": image_id
        })

        return True