from datetime import datetime as dt, timezone
from typing import Any

from src.auth.services import Hasher
from src.authors.exceptions import AuthorNotFoundByIdException
from src.authors.repositories import AuthorRepository
from src.authors.schemas import CreateAuthorRequestSchema
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class AuthorService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session, repo=AuthorRepository(db_session))

    async def get_author_by_id(
            self,
            user_id: int | str
    ) -> dict[str, Any] | None:
        author_data = await self._repo.get_object(id=int(user_id))
        if not author_data:
            raise AuthorNotFoundByIdException
        return author_data

    async def create_author(
            self,
            author_schema: CreateAuthorRequestSchema
    ) -> int:
        author_data = author_schema.model_dump()
        author_data['password'] = Hasher.hash_password(author_schema.password)
        author_data['created_at'] = dt.now(timezone.utc)
        author_id: int = await self._repo.create_object(author_data)
        return author_id
