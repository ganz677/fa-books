import uuid

from fastapi import Form
from pydantic import BaseModel


class AudioCreate(BaseModel):
    title: str
    description: str
    author: str

    @classmethod
    def as_form(
        cls,
        title: str = Form(...),
        description: str = Form(...),
        author: str = Form(...),
    ):
        return cls(title=title, description=description, author=author)



class AudioRead(BaseModel):
    id: int
    title: str
    description: str
    author: str
    filename: str
    uploader_id: uuid.UUID

    class Config:
        from_attributes = True




