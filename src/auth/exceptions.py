from fastapi import HTTPException


class AuthorizationException(HTTPException):
    """Base exception for auth-related errors."""


class WrongCredentialsException(AuthorizationException):
    """Custom exception for when wrong credentials are provided."""

    def __init__(self) -> None:
        """Initialize the WrongCredentialsException with status 404."""
        super().__init__(
            status_code=404,
            detail='User with this credentials can not be found',
        )


class AccessTokenExpiredException(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail='Access token expired')


class RefreshTokenException(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=404,
            detail='Cannot process refresh '
            'token. Probably token '
            "expired, doesn't exist or"
            ' attached to deleted user.',
        )
