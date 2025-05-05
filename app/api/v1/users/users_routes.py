from typing import Annotated

from fastapi import APIRouter, Depends

from .crud import UserCRUD
from .schemas import UserCreate, AuthResponse, UserLogin
from .dependencies import user_crud


router = APIRouter(prefix="/users", tags=["Users"])



@router.post('/register', response_model=AuthResponse)
async def create_new_user(
    user_creds: UserCreate,
    user_dep: Annotated[UserCRUD, Depends(user_crud)]
):
    return await user_dep.create_user(user_creds=user_creds)
    
    
@router.post('/login')
async def user_login(
    user_creds: UserLogin,
    user_dep: Annotated[UserCRUD, Depends(user_crud)]
):
    return await user_dep.user_login(
        username=user_creds.username,
        password=user_creds.password,
    )

