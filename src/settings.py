from functools import cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
COMMON_CONFIG = SettingsConfigDict(
    env_file=BASE_DIR / '.env',
    env_file_encoding='utf-8',
    extra='ignore',
)


class TokenSettings(BaseSettings):
    """Token-related settings."""

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix='TOKEN_'
    )

    SECRET_KEY: str = ''
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30


class DatabaseSettings(BaseSettings):
    """Database-related settings."""
    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix='DB_'
    )

    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.USER}:{self.PASSWORD}"
            f"@{self.HOST}:{self.PORT}/{self.NAME}"
        )


class LoggingSettings(BaseSettings):
    """Logging-related settings."""
    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
        env_prefix='LOGGING_'
    )

    SENTRY_URL: str = ''


class Settings(BaseSettings):
    """Base settings class for the application."""

    model_config = SettingsConfigDict(
        **COMMON_CONFIG,
    )

    # Log level
    LOG_LEVEL: str = 'INFO'
    APP_MODE: str = 'dev'
    # Nested settings
    token_settings: TokenSettings = Field(
        default_factory=TokenSettings
    )
    database_settings: DatabaseSettings = Field(
        default_factory=DatabaseSettings
    )
    logging_settings: LoggingSettings = Field(
        default_factory=LoggingSettings
    )

    @classmethod
    @cache
    def load(cls) -> 'Settings':
        """Return a new instance of Settings."""
        return cls()
