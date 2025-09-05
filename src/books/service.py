from typing import Any
from datetime import datetime as dt, timezone
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.exceptions import BookPermissionException, BookNotFoundException
from src.books.repositories import BookRepository
from src.books.schemas import CreateBookRequestSchema, UpdateBookRequestSchema


class BooksService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session, repo=BookRepository(db_session))

    async def create_book(
            self,
            author: dict[str, Any],
            book_schema: CreateBookRequestSchema,
    ) -> int:
        book_data = book_schema.model_dump()
        book_data['author_id'] = author['id']
        book_data['created_at'] = dt.now(timezone.utc)
        book_id: int = await self._repo.create_object(book_data)
        return book_id

    async def get_book(self, book_id: int):
        book = await self._repo.get_object(id=book_id)
        if not book:
            raise BookNotFoundException
        return book

    async def update_book(
            self,
            author: dict[str, Any],
            book_id: int,
            update_book_schema: UpdateBookRequestSchema
    ):
        book = await self._repo.get_object(id=book_id)
        if not book or author['id'] != book['author_id']:
            raise BookPermissionException
        filtered_book_fields: dict[str, str] = (
            self._validate_schema_for_update_request(update_book_schema)
        )
        updated_book = await self._repo.update_object(
            filtered_book_fields,
            id=book_id
        )
        return updated_book
