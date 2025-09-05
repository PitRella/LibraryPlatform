from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthorRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
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
            return cast(int, result.scalar_one())

    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        conditions = ' AND '.join(f'{key} = :{key}' for key in filters)

        sql = text(f"""
            SELECT id, email, name, biography, birth_year, nationality, created_at, password
            FROM authors
            WHERE {conditions}
            LIMIT 1
        """)

        async with self._session.begin():
            result = await self._session.execute(sql, filters)
            row = result.mappings().first()
            return dict(row) if row else None

    async def delete_object(self, **filters: Any) -> None:
        raise NotImplementedError

    async def update_object(
        self,
        update_data: dict[str, Any],
        **filters: Any,
    ) -> dict[str, Any] | None:
        raise NotImplementedError
