from datetime import UTC
from datetime import datetime as dt
from typing import Annotated

from pydantic import Field

from src.base.schemas import BaseSchema
from src.books.enum import BookGenre, BookLanguage


class CreateBookRequestSchema(BaseSchema):
    """Schema for creating a new book.

    Attributes:
        title (str): Title of the book. 2-50 chars, letters, spaces, hyphens,
                     apostrophes, periods allowed.
        genre (BookGenre): Genre of the book.
        language (BookLanguage): Language of the book.
        published_year (int): Year of publication (1800-current year).

    """

    title: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-\'\.]+$',
            example='Romeo and Juliet',
            description='Book title',
        ),
    ]
    genre: BookGenre
    language: BookLanguage

    published_year: Annotated[
        int,
        Field(
            ge=1800,
            le=dt.now(UTC).year,
            example=1985,
            description='Book published year',
        ),
    ]


class CreateBookResponseSchema(BaseSchema):
    """Schema for response after creating a book.

    Attributes:
        id (int): ID of the newly created book.

    """

    id: int


class UpdateBookRequestSchema(BaseSchema):
    """Schema for updating an existing book.

    All fields are optional and validate constraints as in creation.

    Attributes:
        title (str | None): Updated title, 2-50 chars, letters, spaces,
                            hyphens, apostrophes, periods allowed.
        genre (BookGenre | None): Updated genre.
        language (BookLanguage | None): Updated language.
        published_year (int | None): Updated publication year (1800-current).

    """

    title: Annotated[
        str | None,
        Field(
            default=None,
            min_length=2,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-\'\.]+$',
            example='Romeo and Juliet',
            description='Book title',
        ),
    ]
    genre: BookGenre | None = None
    language: BookLanguage | None = None
    published_year: Annotated[
        int | None,
        Field(
            default=None,
            ge=1800,
            le=dt.now(UTC).year,
            example=1985,
            description='Book published year',
        ),
    ]


class GetBookResponseSchema(BaseSchema):
    """Schema for retrieving book details.

    Attributes:
        id (int): Book ID.
        title (str): Book title.
        genre (BookGenre): Book genre.
        language (BookLanguage): Book language.
        published_year (int): Year the book was published.

    """

    id: int
    title: str
    genre: BookGenre
    language: BookLanguage
    published_year: int


class UploadedBooksResponseSchema(BaseSchema):
    """Schema for response after bulk book import.

    Attributes:
        imported (int): Number of books successfully imported.
        book_ids (list[int]): IDs of imported books.

    """

    imported: int
    book_ids: list[int]


class BookFiltersSchema(BaseSchema):
    """Schema for filtering books.

    Attributes:
        title (str | None): Filter by book title.
        genre (BookGenre | None): Filter by genre.
        language (BookLanguage | None): Filter by language.
        published_year (int | None): Filter by exact published year.
        year_from (int | None): Filter books published from this year.
        year_to (int | None): Filter books published up to this year.
        author_id (int | None): Filter by author ID.

    """

    title: Annotated[
        str | None,
        Field(
            default=None,
            min_length=1,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-\'\.]+$',
            description='Filter by book title',
            examples=['Romeo and Juliet', 'The Shining'],
        ),
    ] = None
    genre: BookGenre | None = None
    language: BookLanguage | None = None
    published_year: Annotated[
        int | None,
        Field(
            default=None,
            ge=1800,
            le=dt.now(UTC).year,
            description='Filter by published year',
            examples=[1985, 2022],
        ),
    ] = None
    year_from: Annotated[
        int | None,
        Field(
            default=None,
            ge=1800,
            le=dt.now(UTC).year,
            description='Filter books published from this year (inclusive)',
        ),
    ] = None
    year_to: Annotated[
        int | None,
        Field(
            default=None,
            ge=1800,
            le=dt.now(UTC).year,
            description='Filter books published up to this year (inclusive)',
        ),
    ] = None
    author_id: Annotated[
        int | None, Field(default=None, ge=0, description='Filter by author ID')
    ] = None


class BookListParamsSchema(BaseSchema):
    """Schema for book list parameters.

    Attributes:
        limit (int): Maximum number of books to return.
        cursor (int | None): Cursor for pagination.
        filters (BookFiltersSchema): Filters for books.

    """

    limit: Annotated[
        int, Field(gt=0, le=100, description='Maximum number of books')
    ]
    cursor: int | None = None
    filters: BookFiltersSchema


class GetBooksListResponseSchema(BaseSchema):
    """Schema for paginated list of books.

    Attributes:
        items (list[GetBookResponseSchema]): List of books.
        next_cursor (int | None): Cursor for next page, if any.

    """

    items: list[GetBookResponseSchema]
    next_cursor: int | None
