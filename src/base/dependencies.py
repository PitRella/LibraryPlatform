from collections.abc import Callable
from typing import Annotated, TypeVar

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.services import BaseService
from src.database import get_db

Service = TypeVar('Service', bound=BaseService)


def get_service[Service](
    service_type: type[Service],
) -> Callable[[AsyncSession], Service]:
    """Dependency factory to provide a service instance for FastAPI routes.

    This function returns a callable that FastAPI can use with Depends().
    It automatically injects an AsyncSession from the database into the
    service constructor.

    Args:
        service_type (type[Service]): The class of the service to instantiate.
            Must inherit from BaseService.

    Returns:
        Callable[[AsyncSession], Service]: A callable suitable for FastAPI
        Depends that returns an instance of the requested service.

    """

    def _get_service(db: Annotated[AsyncSession, Depends(get_db)]) -> Service:
        """Inner function to instantiate the service with a database session.

        Args:
            db (AsyncSession): Database session injected by FastAPI Depends.

        Returns:
            Service: An instance of the requested service class.

        """
        return service_type(db_session=db)  # type: ignore

    return _get_service
