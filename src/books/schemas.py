import re
from datetime import datetime as dt
from typing import Annotated

from pydantic import Field, EmailStr, field_validator

from src.base.schemas import BaseSchema

from src.books.enum import BookGenre, BookLanguage


class CreateBookRequestSchema(BaseSchema):
    title: Annotated[str, Field(
        min_length=2,
        max_length=50,
        pattern=r'^[a-zA-Z\s\-\'\.]+$',
        example="Romeo and Juliet",
        description="Book title"
    )]
    genre: BookGenre
    language: BookLanguage

    published_year: Annotated[int, Field(
        ge=1800,
        le=dt.now().year,
        example=1985,
        description="Book published year"
    )]

class CreateBookResponseSchema(BaseSchema):
    id: int

class UpdateBookRequestSchema(BaseSchema):
    title: Annotated[str | None, Field(
        default=None,
        min_length=2,
        max_length=50,
        pattern=r'^[a-zA-Z\s\-\'\.]+$',
        example="Romeo and Juliet",
        description="Book title"
    )]
    genre: BookGenre | None = None
    language: BookLanguage | None = None
    published_year: Annotated[int | None, Field(
        default=None,
        ge=1800,
        le=dt.now().year,
        example=1985,
        description="Book published year"
    )]


class GetBookResponseSchema(BaseSchema):
    id: int
    title: str
    genre: BookGenre
    language: BookLanguage
    published_year: int


class UploadedBooksResponseSchema(BaseSchema):
    imported: int
    book_ids: list[int]

