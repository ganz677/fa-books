import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from app.api.v1.auth.handlers import AuthHandler
from app.api.v1.auth.managers import UserManager
from app.api.v1.auth.schemas import UserVerifySchema
from app.api.v1.auth.utils.auth_user_validation import get_token_from_cookies


async def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookies)],
    handler: AuthHandler = Depends(AuthHandler),
    manager: UserManager = Depends(UserManager),
) -> UserVerifySchema:
    decoded_token = await handler.decode_access_token(token=token)
    
    user_id = decoded_token.get('user_id')
    session_id = decoded_token.get('session_id')
    
    if not await manager.get_access_token(user_id=user_id, session_id=session_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'Token is invalid'
        )
        
    user = await manager.get_user_by_id(user_id=uuid.UUID(user_id))
    
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f'User not found'
        )
        
    user.session_id = session_id

    return user