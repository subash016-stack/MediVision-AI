from pydantic import BaseModel


class UpdateProfile(BaseModel):

    full_name: str

    phone: str