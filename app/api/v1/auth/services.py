from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
from itsdangerous import BadSignature, URLSafeTimedSerializer

from app.core.settings import settings

from .handlers import AuthHandler
from .managers import UserManager
from .schemas import AuthUser, CreateUser, UserReturnData, UserVerifySchema
from .tasks import send_confirmation_email


class UserService:
    def __init__(
        self,
        manager: UserManager = Depends(UserManager),
        handler: AuthHandler = Depends(AuthHandler),
    ) -> None:
        self.manager = manager
        self.handler = handler
        self.serializer = URLSafeTimedSerializer(secret_key=settings.front.secret_key)

    async def register_user(self, user: AuthUser) -> UserReturnData:
        hashed_password = self.handler.hash_password(user.password)

        new_user = CreateUser(email=user.email, hashed_password=hashed_password)

        user_data = await self.manager.create_user(user=new_user)

        confirmation_token = self.serializer.dumps(user_data.email)

        send_confirmation_email.delay(to_email=user_data.email, token=confirmation_token)

        return user_data

    async def confirm_user(self, token: str):
        try:
            email = self.serializer.loads(token, max_age=360)
        except BadSignature:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Uncorrect or expired token'
            )

        await self.manager.confirm_user(email=email)

    async def login_user(self, user: AuthUser):
        exist_user = await self.manager.get_user_by_email(email=user.email)

        if exist_user is None or not self.handler.verify_password(
            raw_password=user.password,
            hashed_password=exist_user.hashed_password,
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Wrong email or password'
            )

        token, session_id = await self.handler.create_access_token(user_id=exist_user.id)

        await self.manager.store_access_token(
            token=token,
            user_id=exist_user.id,
            session_id=session_id,
        )

        response = JSONResponse(
            content={
                'message': 'Successful authorization'
            }
        )
        response.set_cookie(
            key='Authorization',
            value=token,
            httponly=True,
            max_age=settings.auth_jwt.access_token_lifetime_seconds,
        )

        return response

    async def logout_user(self, user: UserVerifySchema) -> JSONResponse:
        await self.manager.revoke_access_token(user_id=user.id, session_id=user.session_id)

        response = JSONResponse(content={
            'message': 'Logged out'
        })
        response.delete_cookie(key='Authorization')

        return response
