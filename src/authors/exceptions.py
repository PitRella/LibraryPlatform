from fastapi import HTTPException


class AuthorException(HTTPException):
    """Base exception for author-related errors."""


class BadPasswordSchemaException(AuthorException):
    """Raised when the password does not meet the required complexity.

    The password must contain at least one uppercase letter, one lowercase
    letter, one digit, and one special character @$!%*?&.
    """

    def __init__(self) -> None:
        """Initialize BadPasswordSchemaException with status code 422."""
        super().__init__(
            status_code=422,
            detail=(
                'Password should contain at least one uppercase letter, '
                'one lowercase letter, one digit, and one special '
                'character @$!%*?&.'
            ),
        )


class AuthorNotFoundByIdException(AuthorException):
    """Raised when an author with the specified ID does not exist."""

    def __init__(self) -> None:
        """Initialize AuthorNotFoundByIdException with status code 404."""
        super().__init__(
            status_code=404,
            detail='Author by this id not found.',
        )
