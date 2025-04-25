from fastapi import APIRouter

from .authors.authors_routes import router as author_router
from .books.books_routes import router as books_router
from .users.users_routes import router as users_router

router = APIRouter(prefix="/v1")

router.include_router(books_router)
router.include_router(author_router)
router.include_router(users_router)