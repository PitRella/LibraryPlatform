from datetime import datetime as dt, timezone

from src.authors.schemas import CreateAuthorRequestSchema
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


class AuthorService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session)

    async def create_author(self, author_schema: CreateAuthorRequestSchema) -> None:
        # TODO: Add password hash
        sql = text(
            """
            INSERT INTO authors (email, password, name, biography,
                                 birth_year, nationality, created_at)
            VALUES (:email, :password, :name, :biography, :birth_year,
                    :nationality, :created_at) RETURNING id
            """
        )
        params = {
            "email": author_schema.email,
            "password": author_schema.password,  # TODO: Add password hash
            "name": author_schema.name,
            "biography": author_schema.biography,
            "birth_year": author_schema.birth_year,
            "nationality": author_schema.nationality,
            "created_at": dt.now(timezone.utc)
        }
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            author_id = result.scalar_one()
        return author_id
