import re
from datetime import datetime as dt
from typing import Annotated

from pydantic import Field, EmailStr, field_validator

from src.authors.exceptions import BadPasswordSchemaException
from src.base.schemas import BaseSchema
from pydantic import BaseModel

from src.books.enum import BookGenre, BookLanguage

PASSWORD_PATTERN = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)


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

    published_year: Annotated[int | None, Field(
        default=None,
        ge=1800,
        le=dt.now().year,
        example=1985,
        description="Book published year"
    )]

