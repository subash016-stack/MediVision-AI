from pydantic import BaseModel, EmailStr, Field
from typing import Literal


class UserRegister(BaseModel):

    full_name: str = Field(..., min_length=3, max_length=100)

    email: EmailStr

    phone: str = Field(..., min_length=10, max_length=15)

    password: str = Field(..., min_length=8)

    role: Literal["patient", "doctor"]


class UserLogin(BaseModel):

    email: EmailStr

    password: str