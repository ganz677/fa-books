from fastapi import APIRouter
from fastapi_users import FastAPIUsers


from core.models import User
from .backend import auth_backend
from .manager import get_user_manager
from .schemas import UserCreate, UserRead


fastapi_users = FastAPIUsers[User, str](
    get_user_manager,
    [auth_backend],
)

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"]
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"]
)
