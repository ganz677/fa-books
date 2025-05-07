from typing import Annotated

from fastapi import APIRouter, Depends, Form

from api.v1.cruds.user_crud import UserCRUD
from api.v1.schemas.user_schemas import UserCreate, AuthResponse, UserLogin
from api.v1.dependencies import user_dependencies as user_dep

from core.models import User


router = APIRouter(prefix="/users", tags=["Users"])



@router.post('/register', response_model=AuthResponse)
async def create_new_user(
    user_creds: UserCreate,
    user_dep: Annotated[UserCRUD, Depends(user_dep.get_user_crud)]
):
    return await user_dep.create_user(user_creds=user_creds)
    
    
@router.post('/login')
async def user_login(
    username: str = Form(...),
    password: str = Form(...),
    user_crud: UserCRUD = Depends(user_dep.get_user_crud),
):
    return await user_crud.validate_auth_user(
        username=username,
        password=password,
    )


@router.get('/me')
async def get_my_info(
    user: User = Depends(user_dep.get_active_user)
):
    return {
        'id': user.id,
        'username': user.username,
        'email': user.email,
    }