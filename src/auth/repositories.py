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

    async def get_object(self, params: dict[str, Any]) -> Any:
        pass