from typing import Optional

from pydantic import BaseModel


class BookRead(BaseModel):
    id: int
    title: str
    description: str
    num_pages: int


class BookCreate(BookRead):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    num_pages: Optional[int] = None
