import uuid
from calendar import timegm
from datetime import UTC, datetime, timedelta

from jose import JWTError, jwt

from src.auth.exceptions import (
    AccessTokenExpiredException,
    RefreshTokenException,
    WrongCredentialsException,
)
from src.auth.models import RefreshToken
from src.settings import Settings

settings = Settings.load()

type access_token = dict[str, str | datetime]


class TokenManager:

    @classmethod
    def generate_access_token(cls, author_id: int) -> str:
        to_encode: access_token = {
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
        return f'Bearer {encoded_jwt}'

    @classmethod
    def generate_refresh_token(cls) -> tuple[uuid.UUID, timedelta]:

        return uuid.uuid4(), timedelta(
            days=settings.token_settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    @classmethod
    def decode_access_token(cls, token: str) -> dict[str, str | int]:
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
        cls,
        decoded: dict[str, str | int],
    ) -> None:
        jwt_exp_date: int = int(decoded.get('exp', 0))
        current_time: int = timegm(datetime.now(UTC).utctimetuple())
        if not jwt_exp_date or current_time >= jwt_exp_date:
            raise AccessTokenExpiredException

    @classmethod
    def validate_refresh_token_expired(
        cls,
        refresh_token_model: RefreshToken,
    ) -> None:
        current_date: datetime = datetime.now(UTC)
        refresh_token_expire_date: datetime = (
            refresh_token_model.created_at
            + timedelta(seconds=refresh_token_model.expires_in)
        )
        if current_date >= refresh_token_expire_date:
            raise RefreshTokenException
