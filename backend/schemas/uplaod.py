from pydantic import BaseModel


class UploadResponse(BaseModel):
    image_id: str
    image_url: str
