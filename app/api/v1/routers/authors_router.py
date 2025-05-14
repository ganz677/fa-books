from typing import Annotated, List

from api.v1.cruds import author_crud as author_crud
from api.v1.schemas.author_schemas import AuthorCreate, AuthorRead, AuthorUpdate
from core.models import db_helper
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=List[AuthorRead])
async def get_all_authors(
    db: Annotated['AsyncSession', Depends(db_helper.session_getter)]
):
    return await author_crud.get_authors_from_db(db=db)


@router.get("/{author_id}", response_model=AuthorRead)
async def get_author_by_id(
    author_id: int,
    db: AsyncSession = Depends(db_helper.session_getter),
):
    return await author_crud.get_authors_by_id_from_db(author_id=author_id, db=db)


@router.post("/new", response_model=AuthorCreate, status_code=201)
async def add_new_author(
    author_creds: AuthorCreate,
    db: Annotated['AsyncSession', Depends(db_helper.session_getter)]
):
    return await author_crud.create_new_author(author_creds=author_creds, db=db)


@router.delete("/delete")
async def remove_any_author(
    author_id: int,
    db: Annotated['AsyncSession', Depends(db_helper.session_getter)],
):
    return await author_crud.delete_author_by_id(author_id=author_id, db=db)


@router.patch("/change/{author_id}")
async def change_author_info(
    author_id: int,
    update_creds: AuthorUpdate,
    db: Annotated['AsyncSession', Depends(db_helper.session_getter)],
):
    return await author_crud.update_author_data(author_id=author_id, update_creds=update_creds, db=db)



@router.post('/add-book/{book_id}/to-author/{author_id}')
async def add_any_book_to_author(
    book_id: int,
    author_id: int,
    db: Annotated['AsyncSession', Depends(db_helper.session_getter)],
):
    return await author_crud.add_book_to_author(
        book_id=book_id,
        author_id=author_id,
        db=db
    )

