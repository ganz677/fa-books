import uuid
from typing import TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from app.core.models import User, db_helper
from app.core.models.redis_helper import RedisHelper

from .schemas import CreateUser, GetUserWithIDAndEmail, UserReturnData, UserVerifySchema

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class UserManager:
    def __init__(
        self,
        db: 'AsyncSession' = Depends(db_helper.session_getter),
        redis: RedisHelper = Depends(RedisHelper),
    ) -> None:
        self.db = db
        self.redis = redis
        self.model = User

    async def create_user(self, user: CreateUser) -> UserReturnData:
        query = insert(self.model).values(**user.model_dump()).returning(self.model)
        try:
            result = await self.db.execute(query)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="User already exists.")

        await self.db.commit()

        user_data = result.scalar_one()
        return UserReturnData(**user_data.__dict__)


    async def confirm_user(self, email: str) -> None:
        query = update(self.model).where(self.model.email==email).values(is_verified=True, is_active=True)
        try:
            await self.db.execute(query)
            await self.db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='User confirmation failed due to integrity error'
            )

    async def get_user_by_email(self, email: str) -> GetUserWithIDAndEmail:
        query = select(
            self.model.id,
            self.model.email,
            self.model.hashed_password
        ).where(self.model.email == email)
        result = await self.db.execute(query)
        user = result.mappings().first()
        if user:
            return GetUserWithIDAndEmail(**user)
        return None


    async def get_user_by_id(self, user_id: uuid.UUID | str) -> UserVerifySchema | None:
        query = select(self.model.id, self.model.email).where(self.model.id == user_id)
        result = await self.db.execute(query)
        user = result.mappings().one_or_none()

        if user:
            return UserVerifySchema(**user)

        return None

    async def store_access_token(self, token: str, user_id: uuid.UUID, session_id: str) -> None:
        async with self.redis.client_getter() as client:
            await client.set(f"{user_id}:{session_id}", token)


    async def get_access_token(self, user_id: uuid.UUID | str, session_id: str) -> str | None:
        async with self.redis.client_getter() as client:
            return await client.get(f'{user_id}:{session_id}')


    async def revoke_access_token(self, user_id: uuid.UUID | str, session_id: str) -> str:
        async with self.redis.client_getter() as client:
            await client.delete(f'{user_id}:{session_id}')
