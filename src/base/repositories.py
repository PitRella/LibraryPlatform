from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_object(self, params: dict[str, Any]):  # type: ignore
        pass

    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        pass

    async def update_object(
            self,
            update_data: dict[str, Any],
            **filters: Any,
    ) -> dict[str, Any] | None:
        pass

    async def delete_object(
            self,
            **filters: Any
    ) -> None:
        pass
