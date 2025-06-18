import datetime
import uuid

from fastapi import Form
from pydantic import BaseModel, EmailStr


class GetUserByID(BaseModel):
    id: uuid.UUID | str


class GetUserByEmail(BaseModel):
    email: EmailStr


class UserVerifySchema(GetUserByID, GetUserByEmail):
    session_id: uuid.UUID | str | None = None


class CreateUser(GetUserByEmail):
    hashed_password: str


class GetUserWithIDAndEmail(GetUserByID, CreateUser):
    pass


class UserReturnData(GetUserByID, GetUserByEmail):
    is_active: bool
    is_verified: bool
    is_superuser: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class AuthUser(BaseModel):
    email: EmailStr
    password: str

    @classmethod
    def as_form(cls, email: EmailStr = Form(...), password: str = Form(...)):
        return cls(email=email, password=password)

