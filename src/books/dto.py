from dataclasses import dataclass, asdict
from typing import Any

from src.base.dto import BaseDTO
from src.books.enum import BookGenre, BookLanguage


@dataclass
class ImportedBooksDTO(BaseDTO):
    imported: int
    book_ids: list[int]


@dataclass
class GetBooksParamsResponseDTO(BaseDTO):
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
    items: list[dict[str, Any]]
    next_cursor: int | None