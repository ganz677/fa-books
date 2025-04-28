from uuid import UUID

from pydantic import EmailStr

from fastapi_users import schemas


class UserRead(schemas.BaseUser[UUID]):
    pass


class UserCreate(schemas.BaseUserCreate):
    pass