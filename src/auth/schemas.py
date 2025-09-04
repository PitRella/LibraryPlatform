import uuid

from pydantic import BaseModel

from src.base.schemas import BaseSchema


class TokenSchemas(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'Bearer'  # noqa: S105


class CreateRefreshTokenSchema(BaseSchema):
    user_id: int
    refresh_token: uuid.UUID
    expires_in: float
