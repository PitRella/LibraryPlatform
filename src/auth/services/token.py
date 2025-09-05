import uuid
from calendar import timegm
from datetime import UTC, datetime, timedelta
from typing import Any, TypedDict

from jose import JWTError, jwt

from src.auth.exceptions import (
    AccessTokenExpiredException,
    RefreshTokenException,
    WrongCredentialsException,
)
from src.settings import Settings

settings = Settings.load()


class AccessTokenDict(TypedDict):
    sub: str
    exp: datetime


class TokenManager:
    """Manager for creating, decoding, and validating JWT access and refresh tokens."""

    @classmethod
    def generate_access_token(cls, author_id: int) -> str:
        """Generate a JWT access token for the given author ID.

        Args:
            author_id (int): The ID of the author for whom the token is generated.

        Returns:
            str: Encoded JWT access token.

        """
        to_encode: AccessTokenDict = {
            'sub': str(author_id),
            'exp': datetime.now(UTC)
            + timedelta(
                minutes=settings.token_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        }
        encoded_jwt: str = jwt.encode(
            to_encode,
            settings.token_settings.SECRET_KEY,
            algorithm=settings.token_settings.ALGORITHM,
        )
        return encoded_jwt

    @classmethod
    def generate_refresh_token(cls) -> tuple[uuid.UUID, timedelta]:
        """Generate a new refresh token UUID and its expiration timedelta.

        Returns:
            tuple[uuid.UUID, timedelta]: Refresh token and its expiration duration.

        """
        return uuid.uuid4(), timedelta(
            days=settings.token_settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    @classmethod
    def decode_access_token(cls, token: str) -> dict[str, str | int]:
        """Decode a JWT access token to retrieve its payload.

        Args:
            token (str): JWT access token.

        Returns:
            dict[str, str | int]: Decoded token payload.

        Raises:
            WrongCredentialsException: If the token is invalid or cannot be decoded.

        """
        try:
            decoded_jwt: dict[str, str | int] = jwt.decode(
                token=token,
                key=settings.token_settings.SECRET_KEY,
                algorithms=settings.token_settings.ALGORITHM,
            )
        except JWTError:
            raise WrongCredentialsException from None
        return decoded_jwt

    @classmethod
    def validate_access_token_expired(
        cls, decoded: dict[str, str | int]
    ) -> None:
        """Validate whether a decoded JWT access token has expired.

        Args:
            decoded (dict[str, str | int]): Decoded JWT token payload.

        Raises:
            AccessTokenExpiredException: If the token is expired.

        """
        jwt_exp_date: int = int(decoded.get('exp', 0))
        current_time: int = timegm(datetime.now(UTC).utctimetuple())
        if not jwt_exp_date or current_time >= jwt_exp_date:
            raise AccessTokenExpiredException

    @classmethod
    def validate_refresh_token_expired(
        cls, refresh_token_model: dict[str, Any]
    ) -> None:
        """Validate whether a refresh token has expired based on its creation time and expiry.

        Args:
            refresh_token_model (dict[str, Any]): Refresh token record containing `created_at` and `expires_in`.

        Raises:
            RefreshTokenException: If the refresh token is expired.

        """
        current_date: datetime = datetime.now(UTC)
        refresh_token_expire_date: datetime = refresh_token_model[
            'created_at'
        ] + timedelta(seconds=refresh_token_model['expires_in'])
        if current_date >= refresh_token_expire_date:
            raise RefreshTokenException
