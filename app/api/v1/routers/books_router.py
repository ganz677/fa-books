from typing import Annotated, List

from api.v1.cruds import book_crud as book_crud
from api.v1.schemas.book_schemas import BookCreate, BookRead, BookUpdate
from core.models import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/books", tags=["Books"])



@router.get("/", response_model=List[BookRead])
async def get_all_books(
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await book_crud.get_all_books(db=db)


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(
    book_id: int,
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await book_crud.get_book_by_id(book_id=book_id, db=db)


@router.post("/new", response_model=BookCreate, status_code=201)
async def add_new_book(
    book_creds: BookCreate,
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await book_crud.create_new_book(book_creds=book_creds, db=db)


@router.delete("/delete")
async def remove_any_book(
    book_id: int,
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await book_crud.delete_book_by_id(book_id=book_id, db=db)


@router.patch("/change/{book_id}", response_model=BookRead)
async def change_book_info(
    book_id: int,
    update_data: BookUpdate,
    db: Annotated[AsyncSession, Depends(db_helper.session_getter)]
):
    return await book_crud.change_book_creds(book_id=book_id, new_creds=update_data, db=db)
