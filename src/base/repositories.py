from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    """Abstract base class for all repositories.

    Provides basic CRUD interface for database operations. Concrete
    repositories should implement all abstract methods.

    Attributes:
        _session (AsyncSession): SQLAlchemy asynchronous session used for
            database interactions.

    """

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session.

        """
        self._session = session

    @abstractmethod
    async def create_object(self, params: dict[str, Any]) -> int:
        """Create a new object in the repository.

        Args:
            params (dict[str, Any]): Dictionary of fields and values for
                the new object.

        Returns:
            Any: Identifier or representation of the created object.

        """

    @abstractmethod
    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        """Retrieve a single object matching the given filters.

        Args:
            **filters (Any): Keyword arguments to filter the query.

        Returns:
            dict[str, Any] | None: Dictionary of object fields if found,
            otherwise None.

        """

    @abstractmethod
    async def update_object(
        self,
        update_data: dict[str, Any],
        **filters: Any,
    ) -> dict[str, Any] | None:
        """Update an object in the repository matching the given filters.

        Args:
            update_data (dict[str, Any]): Fields and values to update.
            **filters (Any): Keyword arguments to identify the object.

        Returns:
            dict[str, Any] | None: Updated object as a dictionary if found,
            otherwise None.

        """

    @abstractmethod
    async def delete_object(self, **filters: Any) -> None:
        """Delete an object matching the given filters.

        Args:
            **filters (Any): Keyword arguments to identify the object.

        Returns:
            None

        """


class ListableRepository(BaseRepository):
    """Abstract repository that supports listing multiple objects with filters.

    Inherits from BaseRepository. Concrete implementations must define
    `list_objects`.
    """

    @abstractmethod
    async def list_objects(
        self,
        filters: list[str],
        params: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """List objects in the repository that match the provided filters.

        Args:
            filters (list[str]): List of SQL filter expressions.
            params (dict[str, Any]): Dictionary of parameters for query.

        Returns:
            list[dict[str, Any]]: List of objects as dictionaries.

        """
