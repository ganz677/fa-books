from typing import TYPE_CHECKING, List

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from core.models import Book
from api.v1.schemas.book_schemas import BookCreate, BookUpdate


if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class BooksCRUD:
    def __init__(self, db: 'AsyncSession'):
        self.db = db


    async def get_books(
        self
    ) -> List[Book]:
        try: 
            result = await self.db.execute(select(Book))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error {e}'
            ) 


    async def get_book_id(
        self,
        book_id: int,
    ):
        try:
            result = await self.db.execute(select(Book).filter(Book.id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")
            return book
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error {e}'
            )
            


    async def create_book(
        self,
        book_info: BookCreate,
    ):
        try:
            existing_book = await self.db.execute(select(Book).where(Book.title == book_info.title))
            if existing_book.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Author already exists")

            book = Book(**book_info.model_dump())
            self.db.add(book)

            await self.db.commit()
            await self.db.refresh(book)

            return book
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )

    async def delete_book(
        self,
        book_id: int,
    ):
        try:
            book = await self.db.execute(select(Book).where(Book.id == book_id))
            result = book.scalar_one_or_none()
            if result:
                await self.db.delete(result)
                await self.db.commit()
            else:
                raise HTTPException(status_code=404, detail=f"book id not found")
            return {"message": f"author with id: {book_id} deleted successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )
        

    async def update_book(
        self,
        book_id: int,
        update_data: BookUpdate,
    ):
        try:
            result = await self.db.execute(select(Book).where(Book.id == book_id))
            book = result.scalar_one_or_none()

            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(book, field, value)

            await self.db.commit()
            await self.db.refresh(book)

            return book
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )