from typing import Annotated

from api.v1.cruds import user_crud as user_crud
from api.v1.schemas.user_schemas import AuthResponse, UserCreate, UserLogin
from core.models import db_helper
from fastapi import APIRouter, Depends, Form
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/users", tags=["Users"])



@router.post('/register', response_model=AuthResponse)
async def create_new_user(
    user_data: UserCreate,
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await user_crud.register_new_user(user_data=user_data, db=db)


# @router.post('/login')
# async def user_login(
#     username: str = Form(...),
#     password: str = Form(...),
#     user_crud: UserCRUD = Depends(user_dep.get_user_crud),
# ):
#     return await user_crud.validate_auth_user(
#         username=username,
#         password=password,
    # )
