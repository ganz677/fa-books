from typing import TYPE_CHECKING, Annotated

from api.v1.dals.author_dals import AuthorDAL
from api.v1.schemas.author_schemas import AuthorCreate, AuthorUpdate
from auth.auth_user_validation import get_current_user
from core.models import User
from fastapi import Depends

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_authors_from_db(
    db: 'AsyncSession',
):
    dal = AuthorDAL(db=db)
    return await dal.get_authors()


async def get_authors_by_id_from_db(
    author_id: int,
    db: 'AsyncSession',
):
    dal = AuthorDAL(db=db)
    return await dal.get_author_id(author_id=author_id)

async def create_new_author(
    author_creds: AuthorCreate,
    db: 'AsyncSession'
):
    dal = AuthorDAL(db=db)
    return await dal.create_author(author_creds=author_creds)


async def delete_author_by_id(
    author_id: int,
    db: 'AsyncSession',
):
    dal = AuthorDAL(db=db)
    return await dal.delete_author(author_id=author_id)


async def update_author_data(
    author_id: int,
    update_creds: AuthorUpdate,
    db: 'AsyncSession'
):
    dal = AuthorDAL(db=db)
    return await dal.update_author(author_id=author_id, update_data=update_creds)


async def add_book_to_author(
    book_id: int,
    author_id: int,
    db: 'AsyncSession'
):
    dal = AuthorDAL(db=db)
    return await dal.add_book_to_author(author_id=author_id, book_id=book_id)

