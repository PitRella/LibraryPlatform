from typing import Any
from datetime import datetime as dt, timezone
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.exceptions import BookPermissionException, BookNotFoundException
from src.books.repositories import BookRepository
from src.books.schemas import CreateBookRequestSchema, UpdateBookRequestSchema
from fastapi import UploadFile
from src.books.services.importers import BookImporterFactory


class BooksService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession,
            repo: BookRepository | None = None,
    ) -> None:
        super().__init__(db_session, repo or BookRepository(db_session))

    @staticmethod
    def _validate_author_permission(
            book: dict[str, Any] | None,
            author: dict[str, Any]
    ) -> None:
        if not book or author['id'] != book['author_id']:
            raise BookPermissionException

    @staticmethod
    def _format_book_data(
            author: dict[str, Any],
            book_schema: CreateBookRequestSchema
    ) -> dict[str, Any]:
        book_data = book_schema.model_dump()
        book_data['author_id'] = author['id']
        book_data['created_at'] = dt.now(timezone.utc)
        return book_data

    async def create_book(
            self,
            author: dict[str, Any],
            book_schema: CreateBookRequestSchema,
    ) -> int:
        book_data = self._format_book_data(author, book_schema)
        book_id: int = await self._repo.create_object(book_data)
        return book_id

    async def get_book(self, book_id: int) -> dict[str, Any]:
        book = await self._repo.get_object(id=book_id)
        if not book:
            raise BookNotFoundException
        return book

    async def update_book(
            self,
            author: dict[str, Any],
            book_id: int,
            update_book_schema: UpdateBookRequestSchema
    ) -> dict[str, Any]:
        book = await self._repo.get_object(
            id=book_id
        )
        self._validate_author_permission(book, author)
        filtered_book_fields: dict[str, Any] = (
            self._validate_schema_for_update_request(update_book_schema)
        )
        updated_book: dict[str, Any] | None = await self._repo.update_object(
            filtered_book_fields,
            id=book_id
        )
        if not updated_book:
            raise BookNotFoundException
        return updated_book

    async def delete_book(
            self,
            author: dict[str, Any],
            book_id: int,
    ) -> None:
        book = await self._repo.get_object(id=book_id)
        self._validate_author_permission(book, author)
        await self._repo.delete_object(id=book_id)
        return None

    async def get_all_books(
            self,
            limit: int,
            cursor: int | None,
            title: str | None = None,
            genre: str | None = None,
            language: str | None = None,
            published_year: int | None = None,
            author_id: int | None = None,
    ) -> list[dict[str, Any]]:

        filters = []
        params: dict[str, Any] = {"limit": limit}

        if cursor is not None:
            filters.append("id > :cursor")
            params["cursor"] = cursor
        if title is not None:
            filters.append("title = :title")
            params["title"] = title
        if genre is not None:
            filters.append("genre = :genre")
            params["genre"] = genre
        if language is not None:
            filters.append("language = :language")
            params["language"] = language
        if author_id is not None:
            filters.append("author_id = :author_id")
            params["author_id"] = author_id
        if published_year is not None:
            filters.append("published_year = :published_year")
            params["published_year"] = published_year
        return await self._repo.list_objects(filters, params)

    async def import_books(self, author: dict[str, Any], file: UploadFile):
        importer = BookImporterFactory.get_importer(file)
        books_to_create = await importer.parse(file)
        created_ids = []
        for f_book_data in books_to_create:
            book_data = self._format_book_data(
                author,
                CreateBookRequestSchema(**f_book_data)
            )
            book_id = await self._repo.create_object(book_data)
            created_ids.append(book_id)

        return {"imported": len(created_ids), "book_ids": created_ids}
