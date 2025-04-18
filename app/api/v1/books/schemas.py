from typing import Optional

from pydantic import BaseModel


class BookRead(BaseModel):
    id: int
    title: str
    description: str
    num_pages: int
    
    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    title: str
    description: str
    num_pages: int


class BookUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    num_pages: Optional[int] = None


class BookReadForAuthor(BaseModel):
    id: int
    title: str
    num_pages: int