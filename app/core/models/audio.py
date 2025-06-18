import uuid
from typing import TYPE_CHECKING, List

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.time_stamp_mixins import TimeStampMixin
from .playlist import Playlist
from .playlist_audio_association import playlist_audio_association

if TYPE_CHECKING:
    from .user import User


class Audio(TimeStampMixin, Base):
    id: Mapped[int] = mapped_column(
        Integer(),
        primary_key=True,
        autoincrement=True
    )

    title: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text(),
    )

    author: Mapped[str] = mapped_column(
        String(250),
        nullable=False,
    )

    uploader_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey('users.id'),
        nullable=False,
    )

    uploader: Mapped['User'] = relationship(
        'User',
        back_populates='songs'
    )

    filename: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )


    playlists: Mapped[List['Playlist']] = relationship(
        'Playlist',
        secondary=playlist_audio_association,
        back_populates='audios'
    )
