from typing import TYPE_CHECKING

from fastapi import HTTPException, status, Form, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import User
from auth import utils as auth_utils
from api.v1.schemas.user_schemas import UserCreate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession



http_bearer = HTTPBearer()

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

    async def validate_auth_user(
        self,
        username: str = Form(),
        password: str = Form(),
    ) -> dict:
        try:
            result = await self.db.execute(
                select(User).where(User.username == username)
            )

            user = result.scalar_one_or_none()

            if not user or not auth_utils.verify_password(password=password, hashed_password=user.hashed_password):
                raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid username or password'
            )
            if not user.active:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='User inactive'
                )
            
            jwt_payload = {
                'sub': str(user.id),
                'username': user.username,
                'email': user.email,
            }
                
            token = auth_utils.encode_jwt(jwt_payload)
                
            return {
                    'access_token': token,
                    'token_type': 'Bearer',
                }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f'error: {str(e)}'
            )
    
    async def get_current_auth_user(
        self,
        token: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        try:
            payload = auth_utils.decode_jwt(token=token.credentials)
            user_id = payload.get('sub')
            
            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Invalid Token'
                )

            result = await self.db.execute(
                select(User).filter(User.id == int(user_id))
            )
            
            user = result.scalar_one_or_none()
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='User not found'
                )
            return user
        
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Could not validate creds..'
            )
            
        
    async def get_current_auth_active_user(
        self,
        token: HTTPAuthorizationCredentials = Depends(http_bearer)
    ):
        user =  await self.get_current_auth_user(token=token)
        
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='User inactive'
            )
            
        return user