from pydantic import BaseModel


class ReviewRequest(BaseModel):

    doctor_comments: str