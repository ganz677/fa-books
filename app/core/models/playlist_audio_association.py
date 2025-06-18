from typing import List


from sqlalchemy import Table, ForeignKey, Integer, Column 
from sqlalchemy.dialects.postgresql import UUID


from .base import Base



playlist_audio_association = Table(
    'playlist_audio_association',
    Base.metadata,
    Column('playlist_id', UUID(as_uuid=True), ForeignKey('playlists.id'), primary_key=True),
    Column('audio_id', Integer, ForeignKey('audios.id'), primary_key=True),
)