from typing import Annotated, Any

from fastapi import APIRouter, Depends

from src.auth.dependencies import get_author_from_token
from src.base.dependencies import get_service
from src.books.schemas import CreateBookRequestSchema
from src.books.service import BooksService

books_router = APIRouter(prefix='/books', tags=['author'])


@books_router.post('/', description='Create a new book.')
async def create_books(
        author: Annotated[
            dict[str, Any] | None, Depends(get_author_from_token)
        ],
        book_schema: CreateBookRequestSchema,
        service: Annotated[BooksService, Depends(get_service(BooksService))],
) -> None:
    pass