from fastapi import HTTPException


class AuthorException(HTTPException):
    """Base exception for author-related errors."""


class BadPasswordSchemaException(AuthorException):
    """Exception raised for invalid password format."""

    def __init__(self) -> None:
        """Initialize BadPasswordSchemaException with status 422."""
        super().__init__(
            status_code=422,
            detail='Password should contain at least one uppercase letter, '
            'one lowercase letter, one digit, and one special '
            'character @$!%*?&.',
        )


class AuthorNotFoundByIdException(AuthorException):
    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            detail='Author by this id not found.',
        )
