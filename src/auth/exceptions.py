from fastapi import HTTPException


class AuthorizationException(HTTPException):
    """Base exception for all authentication-related errors."""


class WrongCredentialsException(AuthorizationException):
    """Exception raised when provided credentials are invalid.

    Attributes:
        status_code (int): HTTP status code for the exception (401 Unauthorized).
        detail (str): Human-readable explanation of the error.

    """

    def __init__(self) -> None:
        """Initialize WrongCredentialsException with default message and status."""
        super().__init__(
            status_code=401,
            detail='Invalid credentials provided',
        )


class AccessTokenExpiredException(AuthorizationException):
    """Exception raised when an access token has expired.

    Attributes:
        status_code (int): HTTP status code for the exception (401 Unauthorized).
        detail (str): Human-readable explanation indicating token expiry.

    """

    def __init__(self) -> None:
        """Initialize AccessTokenExpiredException with default message."""
        super().__init__(
            status_code=401,
            detail='Access token has expired',
        )


class RefreshTokenException(AuthorizationException):
    """Exception raised when a refresh token is invalid, expired, or cannot be processed.

    Attributes:
        status_code (int): HTTP status code for the exception (403 Forbidden).
        detail (str): Human-readable explanation of the failure.

    """

    def __init__(self) -> None:
        """Initialize RefreshTokenException with default message."""
        super().__init__(
            status_code=403,
            detail=(
                'Cannot process refresh token. It may be expired, invalid, '
                'or attached to a deleted user.'
            ),
        )
