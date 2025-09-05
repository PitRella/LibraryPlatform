import uuid
from typing import Any

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.exceptions import WrongCredentialsException, \
    RefreshTokenException
from src.auth.repositories import AuthRepository
from src.auth.schemas import TokenSchemas, CreateRefreshTokenSchema
from src.auth.services import Hasher
from src.auth.services.token import TokenManager
from src.authors.models import Author
from src.authors.repositories import AuthorRepository
from src.base.repositories import BaseRepository
from src.base.services import BaseService


class AuthService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession,
            auth_repo: BaseRepository | None = None,
            author_repo: BaseRepository | None = None,
    ) -> None:
        super().__init__(db_session,
                         repo=auth_repo or AuthRepository(db_session))
        self._author_repo = author_repo or AuthorRepository(db_session)

    @staticmethod
    def _verify_user_password(author_password: str, password: str) -> None:
        if not author_password or not Hasher.verify_password(password,
                                                             author_password):
            raise WrongCredentialsException

    async def auth_user(self, email: str, password: str) -> dict[str, Any]:
        author_data = await self._author_repo.get_object(email=email)
        if not author_data:
            raise WrongCredentialsException
        author_password = author_data.get('password', '')
        self._verify_user_password(author_password, password)
        return author_data

    async def create_token(self, author_id: int) -> TokenSchemas:
        access_token: str = TokenManager.generate_access_token(
            author_id=author_id)
        refresh_token, tm_delta = TokenManager.generate_refresh_token()
        create_token_schema = CreateRefreshTokenSchema(
            author_id=author_id,
            refresh_token=refresh_token,
            expires_in=tm_delta.total_seconds(),
        )
        await self._repo.create_object(create_token_schema.model_dump())
        return TokenSchemas(
            access_token=access_token,
            refresh_token=str(refresh_token),
        )

    async def refresh_token(self, refresh_token: uuid.UUID) -> TokenSchemas:
        refresh_token_model = await self._repo.get_object(
            refresh_token=refresh_token)
        if not refresh_token_model:
            raise RefreshTokenException
        TokenManager.validate_refresh_token_expired(
            refresh_token_model=refresh_token_model,
        )
        author_id: int = refresh_token_model['author_id']
        author = await self._author_repo.get_object(id=author_id)
        if not author:
            raise RefreshTokenException
        access_token: str = TokenManager.generate_access_token(
            author_id=author_id,
        )
        updated_refresh_token, tm_delta = (
            TokenManager.generate_refresh_token()
        )
        updated_token = await self._repo.update_object(
            {"refresh_token": updated_refresh_token,
             "expires_in": tm_delta.total_seconds()},
            id=refresh_token_model['id'],
        )
        if not updated_token:
            raise RefreshTokenException
        return TokenSchemas(
            access_token=access_token,
            refresh_token=str(updated_refresh_token),
        )

    async def logout_user(
            self,
            refresh_token: str | None,
    ) -> None:
        if not refresh_token:
            raise RefreshTokenException
        refresh_token_model = await self._repo.get_object(
            refresh_token=refresh_token,
        )
        if not refresh_token_model:
            raise RefreshTokenException
        await self._repo.delete_object(id=refresh_token_model['id'])
        return None