from typing import List, Annotated

from fastapi import APIRouter, Depends

from .crud import BooksCRUD
from .dependencies import books_crud
from .schemas import BookCreate, BookRead, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])



@router.get("/", response_model=List[BookRead])
async def get_all_books(
    books_dep: Annotated[BooksCRUD, Depends(books_crud)]
):
    return await books_dep.get_books()


@router.get("/{book_id}", response_model=BookRead)
async def get_book_by_id(
    book_id: int,
    books_dep: Annotated[BooksCRUD, Depends(books_crud)]
):
    return await books_dep.get_book_id(book_id)


@router.post("/new", response_model=BookCreate, status_code=201)
async def add_new_author(
    book: BookCreate,
    books_dep: Annotated[BooksCRUD, Depends(books_crud)]
):
    return await books_dep.create_book(book_info=book)


@router.delete("/delete")
async def remove_any_book(
    book_id: int,
    books_dep: Annotated[BooksCRUD, Depends(books_crud)]
):
    return await books_dep.delete_book(book_id=book_id)


@router.patch("/change/{book_id}", response_model=BookRead)
async def change_book_info(
    book_id: int,
    update_data: BookUpdate,
    books_dep: Annotated[BooksCRUD, Depends(books_crud)]
):
    return await books_dep.update_book(book_id=book_id, update_data=update_data)

