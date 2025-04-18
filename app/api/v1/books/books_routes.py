from typing import List

from core.models import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import create_book, delete_book, get_book_id, get_books, update_book
from .schemas import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


@router.get("/", response_model=List[BookRead])
async def get_all_books(db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_books(db=db)


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(
    book_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_book_id(book_id=book_id, db=db)


@router.post("/new", response_model=BookCreate, status_code=201)
async def add_new_author(
    book: BookCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await create_book(book_info=book, db=db)


@router.delete("/delete")
async def remove_any_book(
    book_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    return await delete_book(db=db, book_id=book_id)


@router.patch("/change/{book_id}")
async def change_book_info(
    book_id: int,
    update_data: BookUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await update_book(db=db, book_id=book_id, update_data=update_data)
