from typing import List, Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import AuthorCRUD
from .dependencies import authors_crud
from .schemas import AuthorCreate, AuthorRead, AuthorUpdate

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorRead])
async def get_all_authors(author_crud: Annotated[AuthorCRUD, Depends(authors_crud)]):
    return await author_crud.get_authors()


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author_by_id(
    author_id: int,
    author_crud: Annotated[AuthorCRUD, Depends(authors_crud)],
):
    return await author_crud.get_author_id(author_id=author_id)


@router.post("/new", response_model=AuthorCreate, status_code=201)
async def add_new_author(
    author_creds: AuthorCreate,
    author_crud: Annotated[AuthorCRUD, Depends(authors_crud)],
):
    return await author_crud.create_author(author_creds=author_creds)


@router.delete("/delete")
async def remove_any_author(
    author_id: int,
    author_crud: Annotated[AuthorCRUD, Depends(authors_crud)]
):
    return await author_crud.delete_author(author_id=author_id)


@router.patch("/change/{author_id}")
async def change_author_info(
    author_id: int,
    update_data: AuthorUpdate,
    author_crud: Annotated[AuthorCRUD, Depends(authors_crud)]
):
    return await author_crud.update_author(author_id=author_id, update_data=update_data)



@router.post('/add-book/{book_id}/to-author/{author_id}')
async def add_any_book_to_author(
    book_id: int,
    author_id: int,
author_crud: Annotated[AuthorCRUD, Depends(authors_crud)]
):
    return await author_crud.add_book_to_author(
        book_id=book_id,
        author_id=author_id,
    )