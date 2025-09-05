from dataclasses import dataclass
from typing import Any

from src.base.dto import BaseDTO
from src.books.enum import BookGenre, BookLanguage


@dataclass
class ImportedBooksDTO(BaseDTO):
    """
    DTO representing the result of a bulk book import.

    Attributes:
        imported (int): Number of books successfully imported.
        book_ids (list[int]): IDs of the imported books.
    """
    imported: int
    book_ids: list[int]


@dataclass
class GetBooksParamsResponseDTO(BaseDTO):
    """
    DTO for filtering and pagination parameters when retrieving books.

    Attributes:
        limit (int | None): Maximum number of books to return.
        cursor (int | None): Cursor for pagination.
        title (str | None): Filter by book title.
        genre (BookGenre | None): Filter by genre.
        language (BookLanguage | None): Filter by language.
        author_id (int | None): Filter by author ID.
        published_year (int | None): Filter by exact published year.
        year_from (int | None): Filter books published from this year (inclusive).
        year_to (int | None): Filter books published up to this year (inclusive).
    """
    limit: int | None = None
    cursor: int | None = None
    title: str | None = None
    genre: BookGenre | None = None
    language: BookLanguage | None = None
    author_id: int | None = None
    published_year: int | None = None
    year_from: int | None = None
    year_to: int | None = None


@dataclass
class GetBooksResponseDTO(BaseDTO):
    """
    DTO for the response when retrieving multiple books.

    Attributes:
        items (list[dict[str, Any]]): List of books as dictionaries.
        next_cursor (int | None): Cursor for the next page of results, if any.
    """
    items: list[dict[str, Any]]
    next_cursor: int | None
