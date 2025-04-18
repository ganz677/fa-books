from datetime import date
from typing import Optional

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    full_name: str
    biography: str
    birthdate: date


class AuthorUpdate(BaseModel):
    full_name: Optional[str] = None
    biography: Optional[str] = None
    birthdate: Optional[date] = None


class AuthorRead(BaseModel):
    id: int
    full_name: str
    biography: str
    birthdate: date

    class Config:
        from_attributes = True
