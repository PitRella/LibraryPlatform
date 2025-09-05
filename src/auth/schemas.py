import uuid

from pydantic import BaseModel

from src.base.schemas import BaseSchema


class TokenSchemas(BaseModel):
    """Schema representing access and refresh tokens.

    This schema is returned after successful authentication and contains
    the JWT tokens needed for API access. The access token is short-lived
    and should be used for API requests, while the refresh token is long-lived
    and used to obtain new access tokens.

    Attributes:
        access_token (str): JWT access token for authentication.
            Expires in 15 minutes by default.
        refresh_token (str): JWT refresh token for obtaining new access tokens.
            Expires in 30 days by default.
        token_type (str): Type of token, always 'Bearer' for this API.

    Example:
        ```json
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "Bearer"
        }
        ```

    """

    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'  # noqa: S105


class CreateRefreshTokenSchema(BaseSchema):
    """Schema for creating a refresh token entry in the database.

    Attributes:
        author_id (int): ID of the author the refresh token belongs to.
        refresh_token (uuid.UUID): The UUID refresh token value.
        expires_in (float): Expiration time in seconds.

    """

    author_id: int
    refresh_token: uuid.UUID
    expires_in: float


class RefreshTokenRequestSchema(BaseSchema):
    """Schema representing a request to refresh an access token.

    Attributes:
        refresh_token (str): The refresh token provided by the client.

    """

    refresh_token: str
