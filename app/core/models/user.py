from typing import List

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .audio import Audio
from .base import Base
from .mixins.id_user_mixin import IDMixin
from .mixins.time_stamp_mixins import TimeStampMixin


class User(IDMixin, TimeStampMixin, Base):

    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_superuser: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    songs: Mapped[List['Audio']] = relationship(
        'Audio',
        back_populates='uploader'
    )
