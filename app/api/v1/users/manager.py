from fastapi import Depends

from fastapi_users import BaseUserManager, IntegerIDMixin

from core.models import User
from core.settings import settings

from .dependencies.users import get_user_db


class UserManager(IntegerIDMixin, BaseUserManager[User, str]):
    reset_password_token_secret = settings.jwt_token.secret_key
    verification_token_secret = settings.jwt_token.secret_key
    
    
async def get_user_manager(user_db = Depends(get_user_db)):
    yield UserManager(user_db=user_db)