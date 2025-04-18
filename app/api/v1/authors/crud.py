from fastapi import HTTPException

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Author, Book
from .schemas import AuthorCreate, AuthorUpdate



async def get_authors(db: AsyncSession):
    result = await db.execute(select(Author).options(selectinload(Author.books)))
    return result.scalars().all()


async def get_author_id(db: AsyncSession, author_id: int):
    result = await db.execute(select(Author).filter(Author.id == author_id))
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


async def create_author(db: AsyncSession, author_creds: AuthorCreate):
    existing_author = await db.execute(
        select(Author).filter(Author.full_name == author_creds.full_name)
    )
    if existing_author.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Author already exists")

    author = Author(**author_creds.model_dump())

    db.add(author)
    await db.commit()
    await db.refresh(author)

    return author


async def delete_author(db: AsyncSession, author_id: int):
    author = await db.execute(select(Author).where(Author.id == author_id))
    result = author.scalar_one_or_none()
    if result:
        await db.delete(result)
        await db.commit()
    else:
        raise HTTPException(status_code=404, detail=f"author id not found")
    return {"message": f"author with id: {author_id} deleted successfully"}


async def update_author(db: AsyncSession, author_id: int, update_data: AuthorUpdate):
    result = await db.execute(select(Author).where(Author.id == author_id))
    author = result.scalar_one_or_none()

    if not author:
        raise HTTPException(status_code=404, detail=f"author id not found")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(author, field, value)

    await db.commit()
    await db.refresh(author)

    return {
        "message": "success",
        "full_name": author.full_name,
        "biography": author.biography,
        "birthdate": author.birthdate,
    }



async def add_book_to_author(
    db: AsyncSession,
    book_id: int,
    author_id: int,
):
    result = await db.execute(
        select(Author)
        .where(Author.id == author_id)
        .options(selectinload(Author.books))
    )
    author = result.scalar_one_or_none()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    result = await db.execute(select(Book).where(Book.id == book_id))
    book = result.scalar_one_or_none()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book in author.books:
        raise HTTPException(status_code=400, detail="Book already added to author")

    author.books.append(book)
    await db.commit()
    await db.refresh(author)
    return {
        'message': 'complete'
    }
        