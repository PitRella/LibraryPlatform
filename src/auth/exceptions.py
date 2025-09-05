from fastapi import HTTPException

class AuthorizationException(HTTPException):
    """Base exception for auth-related errors."""
    pass


class WrongCredentialsException(AuthorizationException):
    """Custom exception for when wrong credentials are provided."""

    def __init__(self) -> None:
        """Initialize the WrongCredentialsException with status 404."""
        super().__init__(
            status_code=404,
            detail='User with this credentials can not be found',
        )
