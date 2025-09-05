from abc import abstractmethod, ABC
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self._session = session

    @abstractmethod
    async def create_object(self, params: dict[str, Any]):  # type: ignore
        pass

    @abstractmethod
    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def update_object(
            self,
            update_data: dict[str, Any],
            **filters: Any,
    ) -> dict[str, Any] | None:
        pass

    @abstractmethod
    async def delete_object(
            self,
            **filters: Any
    ) -> None:
        pass


class ListableRepository(BaseRepository):
    @abstractmethod
    async def list_objects(
            self,
            limit: int = 10,
            cursor: int | None = None
    ) -> list[dict[str, Any]] | None:
        pass
