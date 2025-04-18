from core.models import Author
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from .schemas import AuthorCreate, AuthorUpdate


async def get_authors(db: AsyncSession):
    db.expire_all()
    result = await db.execute(select(Author))
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
