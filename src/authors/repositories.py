from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthorRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def insert_author(self, params: dict[str, Any]) -> int:
        sql = text(
            """
            INSERT INTO authors (email, password, name, biography,
                                 birth_year, nationality, created_at)
            VALUES (:email, :password, :name, :biography, :birth_year,
                    :nationality, :created_at)
            RETURNING id
            """
        )
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            return result.scalar_one()
