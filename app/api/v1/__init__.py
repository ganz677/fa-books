from fastapi import APIRouter

from .routers.authors_router import router as author_router
from .routers.books_router import router as books_router
from .routers.users_router import router as users_router

router = APIRouter(prefix="/v1")

router.include_router(books_router)
router.include_router(author_router)
router.include_router(users_router)