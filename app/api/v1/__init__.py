from fastapi import APIRouter

from .auth.routes import router as users_router
from .audio_downloader.routes import router as audio_router

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(audio_router)