from fastapi import APIRouter

from .audio_downloader.routes import router as audio_router
from .auth.routes import router as users_router

router = APIRouter(prefix="/v1")
router.include_router(users_router)
router.include_router(audio_router)
