from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
        pass

    async def get_object(self, params: dict[str, Any]) -> Any:
        pass