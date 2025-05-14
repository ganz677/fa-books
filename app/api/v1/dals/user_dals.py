from typing import TYPE_CHECKING

from api.v1.schemas.user_schemas import UserCreate
from auth import utils as auth_utils
from core.models import User
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession




class UserDAL:
    def __init__(self, db: 'AsyncSession'):
        self.db = db

    async def create_user(self, user_creds: UserCreate):
        try:
            result = await self.db.execute(
                select(User).filter(User.username == user_creds.username)
            )
            if result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="User already exists")

            user_data = user_creds.model_dump()
            user_data['hashed_password'] = auth_utils.hash_password(user_data.pop('password'))

            user = User(**user_data)

            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)

            token_payload = {
                'sub': str(user.id),
                'username': user.username,
                'email': user.email,
            }
            token = auth_utils.encode_jwt(payload=token_payload)

            return {
                'access_token': token,
                'token_type': 'bearer'
            }

        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )
