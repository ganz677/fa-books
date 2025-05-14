from typing import TYPE_CHECKING

from api.v1.dals.user_dals import UserDAL
from api.v1.schemas.user_schemas import UserCreate, UserLogin, UserRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_user_with_token(
    user_data: UserCreate,
    db: 'AsyncSession'
):
    dal = UserDAL(db=db)
    return await dal.create_user(user_creds=user_data)

async def auth_user_by_password():
    pass
