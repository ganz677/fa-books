from typing import Annotated, List

from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status

from .schemas import AudioRead, AudioCreate
from .services import AudioServices
from ..depends import get_current_user

router = APIRouter(
    prefix='/audio',
    tags=['Audio']
)


@router.post(
    path='/upload_song',
    response_model=AudioRead
)
async def upload_audio_to_server(
    audio_data: Annotated[AudioCreate, Depends(AudioCreate.as_form)],
    service: Annotated[AudioServices, Depends(AudioServices)],
    user_token = Depends(get_current_user),
    file: UploadFile = File(...),
):
    return await service.save_audio(audio_data=audio_data, file=file, uploader_id=user_token.id)



@router.get(
    path='/check_my_uploaded_songs',
    response_model=List[AudioRead],
)
async def all_songs_by_current_user(
    service: Annotated[AudioServices, Depends(AudioServices)],
    user_token = Depends(get_current_user),
):
    return await service.get_songs(user_id=user_token.id)




