import uuid
from typing import Annotated

from fastapi import Depends, HTTPException, status

from .manager import AudioManager
from .schemas import AudioCreate
from ..auth.handlers import AuthHandler


class AudioServices:
    def __init__(self, manager: Annotated[AudioManager, Depends(AudioManager)]):
        self.manager = manager
        
        
    async def save_audio(self, audio_data: AudioCreate, file, uploader_id):
        return await self.manager.upload_audio(audio_data, file, uploader_id)
    
    
    
    async def get_songs(self, user_id = uuid.UUID | str):
        return await self.manager.get_all_songs_by_any_user_from_db(user_id=user_id)