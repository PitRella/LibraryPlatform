import re
from datetime import datetime as dt
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.authors.exceptions import BadPasswordSchemaException
from src.base.schemas import BaseSchema

PASSWORD_PATTERN = re.compile(
    r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
)


class CreateAuthorRequestSchema(BaseSchema):
    """Schema for creating a new author.

    Validates email, password, name, and optional fields like biography,
    birth year, and nationality.
    """

    email: Annotated[
        EmailStr,
        Field(
            min_length=6,
            max_length=128,
            example='potato@gmail.com',
            description="Author's email address",
        ),
    ]

    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=128,
            example='Abc123@xyz',
            description='Password must contain: lowercase, uppercase, '
            'digit, special character',
        ),
    ]

    name: Annotated[
        str,
        Field(
            min_length=2,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-\'\.]+$',
            example='John Smith',
            description="Author's full name",
        ),
    ]

    biography: Annotated[
        str | None,
        Field(
            default=None,
            min_length=16,
            max_length=512,
            pattern=r'^[a-zA-Z0-9\s\.\,\!\?\-\'\"]+$',
            example='I am a passionate writer who loves creating fictional worlds.',
            description="Author's biography",
        ),
    ]

    birth_year: Annotated[
        int | None,
        Field(
            default=None,
            ge=1900,
            le=dt.now().year,
            example=1985,
            description="Author's year of birth",
        ),
    ]

    nationality: Annotated[
        str | None,
        Field(
            default=None,
            min_length=2,
            max_length=50,
            pattern=r'^[a-zA-Z\s\-]+$',
            example='United Kingdom',
            description="Author's nationality",
        ),
    ]

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        """Validate that the password meets complexity requirements.

        Raises:
            BadPasswordSchemaException: If password does not contain
            at least one uppercase letter, one lowercase letter, one digit,
            and one special character @$!%*?&.

        Returns:
            str: The validated password.

        """
        if not PASSWORD_PATTERN.match(value):
            raise BadPasswordSchemaException()
        return value


class CreateAuthorResponseSchema(BaseSchema):
    """Response schema returned after creating a new author.

    Attributes:
        id (int): ID of the newly created author.

    """

    id: int


class GetAuthorResponseSchema(BaseModel):
    """Schema for retrieving author details.

    Attributes:
        email (EmailStr): Author's email address.
        name (str): Author's full name.
        biography (str): Author's biography.
        birth_year (int): Author's year of birth.
        nationality (str): Author's nationality.

    """

    email: EmailStr
    name: str
    biography: str
    birth_year: int
    nationality: str
