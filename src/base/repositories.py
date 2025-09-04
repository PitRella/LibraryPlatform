from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_object(self, params: dict[str, Any]):  # type: ignore
        pass