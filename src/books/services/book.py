from datetime import UTC
from datetime import datetime as dt
from typing import Any

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.services import BaseService
from src.books.dto import (
    GetBooksParamsResponseDTO,
    GetBooksResponseDTO,
    ImportedBooksDTO,
)
from src.books.enum import BookGenre, BookLanguage
from src.books.exceptions import BookNotFoundException, BookPermissionException
from src.books.repositories import BookRepository
from src.books.schemas import CreateBookRequestSchema, UpdateBookRequestSchema
from src.books.services.importers import BookImporterFactory


class BooksService(BaseService):
    """Service layer for managing books.

    Provides methods to create, retrieve, update, delete, list, and import
    books. Ensures proper author permissions and formats book data before
    database operations.

    Attributes:
        db_session (AsyncSession): Async database session for operations.
        _repo (BookRepository): Repository instance for book data access.

    """

    def __init__(
        self,
        db_session: AsyncSession,
        repo: BookRepository | None = None,
    ) -> None:
        """Initialize BooksService with a database session and optional repo.

        Args:
            db_session (AsyncSession): The async session to interact with DB.
            repo (BookRepository | None): Optional custom book repository.

        """
        super().__init__(db_session, repo or BookRepository(db_session))

    @staticmethod
    def _validate_author_permission(
        book: dict[str, Any] | None, author: dict[str, Any]
    ) -> None:
        """Raise exception if the author does not own the book.

        Args:
            book (dict[str, Any] | None): Book data to validate.
            author (dict[str, Any]): Author data performing the action.

        Raises:
            BookPermissionException: If author does not have permission.

        """
        if not book or author['id'] != book['author_id']:
            raise BookPermissionException

    @staticmethod
    def _format_book_data(
        author: dict[str, Any], book_schema: CreateBookRequestSchema
    ) -> dict[str, Any]:
        """Prepare book data for creation or import.

        Adds author ID and creation timestamp to the schema data.

        Args:
            author (dict[str, Any]): Author information.
            book_schema (CreateBookRequestSchema): Schema with book fields.

        Returns:
            dict[str, Any]: Formatted book data.

        """
        book_data = book_schema.model_dump()
        book_data['author_id'] = author['id']
        book_data['created_at'] = dt.now(UTC)
        return book_data

    async def create_book(
        self,
        author: dict[str, Any],
        book_schema: CreateBookRequestSchema,
    ) -> int:
        """Create a new book record in the database.

        Args:
            author (dict[str, Any]): Author creating the book.
            book_schema (CreateBookRequestSchema): Book data schema.

        Returns:
            int: ID of the newly created book.

        """
        book_data = self._format_book_data(author, book_schema)
        book_id: int = await self._repo.create_object(book_data)
        return book_id

    async def get_book(self, book_id: int) -> dict[str, Any]:
        """Retrieve a book by its ID.

        Args:
            book_id (int): Unique identifier of the book.

        Returns:
            dict[str, Any]: Book data.

        Raises:
            BookNotFoundException: If the book does not exist.

        """
        book = await self._repo.get_object(id=book_id)
        if not book:
            raise BookNotFoundException
        return book

    async def update_book(
        self,
        author: dict[str, Any],
        book_id: int,
        update_book_schema: UpdateBookRequestSchema,
    ) -> dict[str, Any]:
        """Update an existing book's data.

        Args:
            author (dict[str, Any]): Author performing the update.
            book_id (int): ID of the book to update.
            update_book_schema (UpdateBookRequestSchema): Updated fields.

        Returns:
            dict[str, Any]: Updated book data.

        Raises:
            BookPermissionException: If author is not allowed to update.
            BookNotFoundException: If book does not exist.

        """
        book = await self._repo.get_object(id=book_id)
        self._validate_author_permission(book, author)
        filtered_book_fields: dict[str, Any] = (
            self._validate_schema_for_update_request(update_book_schema)
        )
        updated_book: dict[str, Any] | None = await self._repo.update_object(
            filtered_book_fields, id=book_id
        )
        if not updated_book:
            raise BookNotFoundException
        return updated_book

    async def delete_book(
        self,
        author: dict[str, Any],
        book_id: int,
    ) -> None:
        """Delete a book by ID if author has permission.

        Args:
            author (dict[str, Any]): Author requesting deletion.
            book_id (int): ID of the book to delete.

        Raises:
            BookPermissionException: If author cannot delete the book.
            BookNotFoundException: If book does not exist.

        """
        book = await self._repo.get_object(id=book_id)
        self._validate_author_permission(book, author)
        await self._repo.delete_object(id=book_id)

    async def get_all_books(
        self,
        limit: int,
        cursor: int | None,
        title: str | None = None,
        genre: str | None = None,
        language: str | None = None,
        published_year: int | None = None,
        author_id: int | None = None,
        year_from: int | None = None,
        year_to: int | None = None,
    ) -> GetBooksResponseDTO:
        """List books with optional filters and pagination.

        Supports filtering by title, genre, language, author, and year.

        Args:
            limit (int): Maximum number of books to return.
            cursor (int | None): Cursor for pagination.
            title (str | None): Filter by book title.
            genre (str | None): Filter by book genre.
            language (str | None): Filter by book language.
            published_year (int | None): Filter by publication year.
            author_id (int | None): Filter by author ID.
            year_from (int | None): Filter books published from this year.
            year_to (int | None): Filter books published up to this year.

        Returns:
            GetBooksResponseDTO: Paginated books and next cursor.

        """
        filters: list[str] = []
        params_d = GetBooksParamsResponseDTO(limit=limit + 1)
        if cursor is not None:
            filters.append('id > :cursor')
            params_d.cursor = cursor
        if title is not None:
            filters.append('title = :title')
            params_d.title = title
        if genre is not None:
            filters.append('genre = :genre')
            params_d.genre = BookGenre(genre)
        if language is not None:
            filters.append('language = :language')
            params_d.language = BookLanguage(language)
        if author_id is not None:
            filters.append('author_id = :author_id')
            params_d.author_id = author_id
        if published_year is not None:
            filters.append('published_year = :published_year')
            params_d.published_year = published_year
        if year_from is not None:
            filters.append('published_year >= :year_from')
            params_d.year_from = year_from
        if year_to is not None:
            filters.append('published_year <= :year_to')
            params_d.year_to = year_to
        rows = await self._repo.list_objects(filters, params_d.to_dict())  # type: ignore
        items = rows[:limit]
        next_cursor = items[-1]['id'] if len(rows) > limit else None
        return GetBooksResponseDTO(items=items, next_cursor=next_cursor)

    async def import_books(
        self, author: dict[str, Any], file: UploadFile
    ) -> ImportedBooksDTO:
        """Bulk import books from a CSV or JSON file.

        Args:
            author (dict[str, Any]): Author importing the books.
            file (UploadFile): File containing books data.

        Returns:
            ImportedBooksDTO: Number of books imported and their IDs.

        """
        importer = BookImporterFactory.get_importer(file)
        books_to_create = await importer.parse(file)
        created_ids: list[int] = []
        for f_book_data in books_to_create:
            book_data = self._format_book_data(
                author, CreateBookRequestSchema(**f_book_data)
            )
            book_id = await self._repo.create_object(book_data)
            created_ids.append(book_id)
        return ImportedBooksDTO(imported=len(created_ids), book_ids=created_ids)
