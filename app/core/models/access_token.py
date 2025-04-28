from typing import TYPE_CHECKING

from uuid import UUID

from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyBaseAccessTokenTableUUID,
    SQLAlchemyAccessTokenDatabase
)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
 

from .base import Base

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AccessToken(Base, SQLAlchemyBaseAccessTokenTableUUID):
    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey('users.id', ondelete='CASCADE'),
        nullable=False,
    )
    
    @classmethod
    def get_db(cls, session: 'AsyncSession'):
        return SQLAlchemyAccessTokenDatabase(session, cls)
    
    