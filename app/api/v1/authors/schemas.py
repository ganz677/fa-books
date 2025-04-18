from typing import List

from datetime import date
from typing import Optional

from pydantic import BaseModel

from api.v1.books.schemas import BookReadForAuthor

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
    books: List[BookReadForAuthor]

    class Config:
        from_attributes = True
