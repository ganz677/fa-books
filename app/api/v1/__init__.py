from fastapi import APIRouter

from .auth.routes import router as users_router

router = APIRouter(prefix="/v1")

# router.include_router(books_router)
# router.include_router(author_router)
router.include_router(users_router)
