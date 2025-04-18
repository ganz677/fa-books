from typing import List

from core.models import db_helper
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import (
    create_author,
    delete_author,
    get_author_id,
    get_authors,
    update_author,
)
from .schemas import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorRead])
async def get_all_authors(db: AsyncSession = Depends(db_helper.session_getter)):
    return await get_authors(db=db)


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author_by_id(
    author_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await get_author_id(author_id=author_id, db=db)


@router.post("/new", response_model=AuthorCreate, status_code=201)
async def add_new_author(
    author: AuthorCreate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await create_author(author_creds=author, db=db)


@router.delete("/delete")
async def remove_any_author(
    author_id: int, db: AsyncSession = Depends(db_helper.session_getter)
):
    return await delete_author(db=db, author_id=author_id)


@router.patch("/change/{author_id}")
async def change_author_info(
    author_id: int,
    update_data: AuthorUpdate,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await update_author(db=db, author_id=author_id, update_data=update_data)
