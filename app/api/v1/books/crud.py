from core.models import Book
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import BookCreate, BookUpdate


async def get_books(
    db: AsyncSession,
):
    db.expire_all()
    result = await db.execute(select(Book))
    return result.scalars().all()


async def get_book_id(
    db: AsyncSession,
    book_id: int,
):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


async def create_book(
    book_info: BookCreate,
    db: AsyncSession,
):
    existing_book = await db.execute(select(Book).where(Book.title == book_info.title))
    if existing_book.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Author already exists")

    book = Book(**book_info.model_dump())
    db.add(book)

    await db.commit()
    await db.refresh(book)

    return book


async def delete_book(
    db: AsyncSession,
    book_id: int,
):
    book = await db.execute(select(Book).where(Book.id == book_id))
    result = book.scalar_one_or_none()
    if result:
        await db.delete(result)
        await db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"book id not found")
    return {"message": f"author with id: {book_id} deleted successfully"}


async def update_book(
    db: AsyncSession,
    book_id: int,
    update_data: BookUpdate,
):
    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()

    if not book:
        raise HTTPException(status_code=404, detail=f"author id not found")

    for field, value in update_data.model_dump().items():
        setattr(book, field, value)

    await db.commit()
    await db.refresh(book)

    return {
        "message": "success",
        "title": book.title,
        "description": book.description,
        "num_pages": book.num_pages,
    }
