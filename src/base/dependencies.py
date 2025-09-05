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
    def _get_service(db: Annotated[AsyncSession, Depends(get_db)]) -> Service:
        return service_type(db_session=db)  # type: ignore

    return _get_service
