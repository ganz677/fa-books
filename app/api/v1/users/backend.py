
from typing import Annotated


from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy.db import DatabaseStrategy
from fastapi import Depends

from ..dependencies.access_tokens import get_access_tokens_db
from core.settings import settings
from core.models import AccessToken

from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

bearer_transport = BearerTransport(tokenUrl="/auth/jwt/login")

def get_database_strategy(
    access_token_db: Annotated[
        SQLAlchemyAccessTokenDatabase[AccessToken],
        Depends(get_access_tokens_db)
    ]
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.jwt_token.lifetime_seconds,
    )

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,  
    get_strategy=get_database_strategy,
)
