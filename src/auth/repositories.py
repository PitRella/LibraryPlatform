from typing import Any
from sqlalchemy import text

from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
        sql = text("""
                   INSERT INTO refresh_tokens (author_id, refresh_token,
                                               expires_in, created_at)
                   VALUES (:author_id, :refresh_token, :expires_in, NOW())
                   RETURNING id
                   """)
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            return result.scalar_one()


    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        conditions = " AND ".join(f"{key} = :{key}" for key in filters.keys())

        sql = text(f"""
                    SELECT id, author_id, refresh_token, expires_in, created_at
                    FROM refresh_tokens
                    WHERE {conditions}
                    LIMIT 1
                """)

        async with self._session.begin():
            result = await self._session.execute(sql, filters)
            row = result.mappings().first()
            return dict(row) if row else None

    async def update_object(
        self,
        update_data: dict[str, Any],
        **filters: Any,
    ) -> dict[str, Any] | None:
        set_expr = ", ".join(f"{k} = :set_{k}" for k in update_data.keys())
        conditions = " AND ".join(f"{k} = :{k}" for k in filters.keys())
        returning = ", ".join(self.fields)

        params = {**{f"set_{k}": v for k, v in update_data.items()}, **filters}

        sql = text(f"""
            UPDATE refresh_tokens
            SET {set_expr}
            WHERE {conditions}
            RETURNING {returning}
        """)
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            row = result.mappings().first()
            return dict(row) if row else None