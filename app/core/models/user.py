from sqlalchemy import String, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        server_default=text('true'),
    )
    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default=text('false')
    )
    
    