from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper
from api.v1.cruds.user_crud import UserCRUD


def get_user_crud(db: Annotated[AsyncSession, Depends(db_helper.session_getter)]) -> UserCRUD:
    return UserCRUD(db=db)
    
    
async def get_current_user(
    crud: Annotated[UserCRUD, Depends(get_user_crud)]
):
    return await crud.get_current_auth_user()


async def get_active_user(
    crud: Annotated[UserCRUD, Depends(get_user_crud)]
):
    return await crud.get_current_auth_active_user()
    