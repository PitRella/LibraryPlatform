from datetime import datetime as dt, timezone
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

    async def create_author(
            self,
            author_schema: CreateAuthorRequestSchema
    ) -> int:
        author_data = author_schema.model_dump()
        # user_data['password'] = # TODO: Add password hash
        author_data['created_at'] = dt.now(timezone.utc)
        author_id: int = await self._repo.create_object(author_data)
        return author_id
