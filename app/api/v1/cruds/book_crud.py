from typing import TYPE_CHECKING

from api.v1.dals.book_dals import BookDAL
from api.v1.schemas.book_schemas import BookCreate, BookUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def get_all_books(
    db: 'AsyncSession'
):
    dal = BookDAL(db=db)
    return await dal.get_books()

async def get_book_by_id(
    book_id: int,
    db: 'AsyncSession'
):
    dal = BookDAL(db=db)
    return await dal.get_book_id(book_id=book_id)


async def create_new_book(
    book_creds: BookCreate,
    db: 'AsyncSession'
):
    dal = BookDAL(db=db)
    return await dal.create_book(book_creds=book_creds)


async def delete_book_by_id(
    book_id: int,
    db: 'AsyncSession'
):
    dal = BookDAL(db=db)
    return await dal.delete_book(book_id=book_id)

async def change_book_creds(
    book_id: int,
    new_creds: BookUpdate,
    db: 'AsyncSession'
):
    dal = BookDAL(db=db)
    return await dal.update_book(book_id=book_id, update_data=new_creds)
