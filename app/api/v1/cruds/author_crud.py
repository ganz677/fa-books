from typing import TYPE_CHECKING

from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from core.models import Author, Book
from api.v1.schemas.author_schemas import AuthorCreate, AuthorUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession



class AuthorCRUD:
    def __init__(self, db: 'AsyncSession'):
        self.db = db

    async def get_authors(self):
        try:
            result = await self.db.execute(select(Author).options(selectinload(Author.books)))
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )

    async def get_author_id(self, author_id: int):
        try:  
            result = await self.db.execute(
                select(Author).options(selectinload(Author.books)).filter(Author.id == author_id)
                )

            author = result.scalar_one_or_none()
            if not author:
                raise HTTPException(status_code=404, detail="Author not found")
            return author
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )
            

    async def create_author(self, author_creds: AuthorCreate):
        try:
            existing_author = await self.db.execute(
                select(Author).filter(Author.full_name == author_creds.full_name)
            )
            if existing_author.scalar_one_or_none():
                raise HTTPException(status_code=400, detail="Author already exists")

            author = Author(**author_creds.model_dump())

            self.db.add(author)
            await self.db.commit()
            await self.db.refresh(author)

            return author
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )

    async def delete_author(self, author_id: int):
        try:
            author = await self.db.execute(select(Author).where(Author.id == author_id))
            result = author.scalar_one_or_none()
            if result:
                await self.db.delete(result)
                await self.db.commit()
            else:
                raise HTTPException(status_code=404, detail=f"author id not found")
            return {"message": f"author with id: {author_id} deleted successfully"}
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )

    async def update_author(self, author_id: int, update_data: AuthorUpdate):
        try:
            result = await self.db.execute(select(Author).where(Author.id == author_id))
            author = result.scalar_one_or_none()

            if not author:
                raise HTTPException(status_code=404, detail=f"author id not found")

            for field, value in update_data.model_dump(exclude_unset=True).items():
                setattr(author, field, value)

            await self.db.commit()
            await self.db.refresh(author)

            return {
                "message": "success",
                "full_name": author.full_name,
                "biography": author.biography,
                "birthdate": author.birthdate,
            }
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )


    async def add_book_to_author(
        self,
        book_id: int,
        author_id: int,
    ):
        try:
            result = await self.db.execute(
                select(Author)
                .where(Author.id == author_id)
                .options(selectinload(Author.books))
            )
            author = result.scalar_one_or_none()
            if not author:
                raise HTTPException(status_code=404, detail="Author not found")

            result = await self.db.execute(select(Book).where(Book.id == book_id))
            book = result.scalar_one_or_none()
            if not book:
                raise HTTPException(status_code=404, detail="Book not found")

            if book in author.books:
                raise HTTPException(status_code=400, detail="Book already added to author")

            author.books.append(book)
            await self.db.commit()
            await self.db.refresh(author)
            return {
                'message': 'complete'
            }
        except SQLAlchemyError as e:
            raise HTTPException(
                status_code=500,
                detail=f'Database error: {e}'
            )
        