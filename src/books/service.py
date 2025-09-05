from typing import Any
from datetime import datetime as dt, timezone
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.repositories import BookRepository
from src.books.schemas import CreateBookRequestSchema


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