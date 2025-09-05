from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.auth.dependencies import get_author_from_token
from src.base.dependencies import get_service
from src.books.schemas import CreateBookRequestSchema, GetBookResponseSchema
from src.books.service import BooksService

books_router = APIRouter(prefix='/books', tags=['books'])


@books_router.post('/',
                   description='Create a new book.')  # TODO: Return id or 204
async def create_book(
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        book_schema: CreateBookRequestSchema,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> None:
    await service.create_book(author, book_schema)


@books_router.get('/{book_id}', description='Get a book')
async def get_book(
        book_id: int,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> GetBookResponseSchema:
    book_data = await service.get_book(book_id)
    return GetBookResponseSchema.model_validate(book_data)
