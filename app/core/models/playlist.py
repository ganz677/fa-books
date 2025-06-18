from typing import List, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .mixins.id_user_mixin import IDMixin
from .mixins.time_stamp_mixins import TimeStampMixin
from .base import Base
from .playlist_audio_association import playlist_audio_association

if TYPE_CHECKING:
    from .audio import Audio

class Playlist(IDMixin, TimeStampMixin, Base):
    
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )
    
    audios: Mapped[List['Audio']] = relationship(
        'Audio',
        secondary=playlist_audio_association,
        back_populates='playlists',
    )
