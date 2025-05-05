from typing import TYPE_CHECKING

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import User
from auth import utils as auth_utils
from .schemas import UserCreate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession



class UserCRUD:
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


    async def user_login(
        self,
        username: str,
        password: str,
):
        try: 
            result = await self.db.execute(
                select(User).where(User.username == username)
            )
            
            user = result.scalar_one_or_none() 
            
            if not user:
                raise HTTPException(
                    status_code=404,
                    detail=f'Username is incorrect'
                )
            
            if not auth_utils.verify_password(password, user.hashed_password) :
                raise HTTPException(
                    status_code=401,
                    detail=f'Password is incorrect'
                )
                
            token = auth_utils.encode_jwt({
                'sub': str(user.id)
            })
            
            return {
                'access_token': token,
                'token_type': 'bearer',
            }
            
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f'Login failed: {str(e)}'
            )