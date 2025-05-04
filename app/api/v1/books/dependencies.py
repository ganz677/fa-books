from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .crud import BooksCRUD


def books_crud(db: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> BooksCRUD:
    return BooksCRUD(db=db)
    