from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserRegister(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    password: str

    role: str


class UserLogin(BaseModel):

    email: EmailStr

    password: str


class UserResponse(BaseModel):

    full_name: str

    email: EmailStr

    phone: str

    role: str

    created_at: datetime