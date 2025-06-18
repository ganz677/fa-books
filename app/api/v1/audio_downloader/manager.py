import shutil
import uuid
from typing import TYPE_CHECKING, Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.core.models import Audio, db_helper
from app.core.settings import settings

from .schemas import AudioCreate, AudioRead

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class AudioManager:
    def __init__(self, db: Annotated['AsyncSession', Depends(db_helper.session_getter)]):
        self.db = db

    async def upload_audio(self, audio_data: AudioCreate, file, uploader_id: uuid.UUID) -> Audio:
        media_dir = settings.audio_settings.audios_dir
        media_dir.mkdir(parents=True, exist_ok=True)

        file_path = media_dir / file.filename

        with file.file as src, open(file_path, 'wb') as dst:
            shutil.copyfileobj(src, dst)

        audio = Audio(
            title = audio_data.title,
            description = audio_data.description,
            author = audio_data.author,
            uploader_id = uploader_id,
            filename = file.filename,
        )

        try:
            self.db.add(audio)
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Audio already exist',
            )

        await self.db.commit()
        await self.db.refresh(audio)

        return audio



    async def get_all_songs_by_any_user_from_db(self, user_id: uuid.UUID) -> list[Audio]:
        query = select(Audio).where(Audio.uploader_id == uuid.UUID(str(user_id)))

        try:
            result = await self.db.execute(query)
        except Exception:
            raise HTTPException(
                status_code=500,
                detail='Database error'
            )

        songs = result.scalars().all()

        if not songs:
            raise HTTPException(status_code=404, detail='No uploaded songs found')

        return songs


