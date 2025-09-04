from src.authors.schemas import CreateAuthorRequestSchema
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession


class AuthorService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session)

    def create_author(self, author_schema: CreateAuthorRequestSchema) -> None:
        raise NotImplementedError()
