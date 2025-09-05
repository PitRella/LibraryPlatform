from typing import Any, final

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository
from src.books.exceptions import ForgottenParametersException


class BaseService:
    def __init__(self, db_session: AsyncSession, repo: BaseRepository) -> None:
        self._session: AsyncSession = db_session
        self._repo: BaseRepository = repo

    @staticmethod
    @final
    def _validate_schema_for_update_request(
        schema: BaseModel,
    ) -> dict[str, Any]:
        schema_fields: dict[str, str] = schema.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )  # Delete None key value pair
        if not schema_fields:
            raise ForgottenParametersException
        return schema_fields
