from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.auth.dependencies import get_author_from_token
from src.base.dependencies import get_service
from src.books.schemas import CreateBookRequestSchema, GetBookResponseSchema, \
    UpdateBookRequestSchema, CreateBookResponseSchema
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
) -> CreateBookResponseSchema:
    book_id: int = await service.create_book(author, book_schema)
    return CreateBookResponseSchema(id=book_id)

@books_router.get('/{book_id}', description='Get a book')
async def get_book(
        book_id: int,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> GetBookResponseSchema:
    book_data = await service.get_book(book_id)
    return GetBookResponseSchema.model_validate(book_data)


@books_router.patch('/{book_id}', description='Change book parameters')
async def update_book(
        book_id: int,
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        update_book_schema: UpdateBookRequestSchema,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> GetBookResponseSchema:
    updated_book = await service.update_book(
        author=author,
        book_id=book_id,
        update_book_schema=update_book_schema
    )
    return GetBookResponseSchema.model_validate(updated_book)

@books_router.delete('/{book_id}', description='Delete book', status_code=204)
async def delete_book(
        book_id: int,
        author: Annotated[
            dict[str, Any], Depends(get_author_from_token)
        ],
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> None:
    updated_book = await service.delete_book(
        author=author,
        book_id=book_id,
    )
