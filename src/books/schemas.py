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
            le=dt.now().year,
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
            le=dt.now().year,
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


class GetBooksListResponseSchema(BaseSchema):
    """Schema for paginated list of books.

    Attributes:
        items (list[GetBookResponseSchema]): List of books.
        next_cursor (int | None): Cursor for next page, if any.

    """

    items: list[GetBookResponseSchema]
    next_cursor: int | None
