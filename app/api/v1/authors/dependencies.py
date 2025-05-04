from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from .crud import AuthorCRUD


def authors_crud(db: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> AuthorCRUD:
    return AuthorCRUD(db=db)
    