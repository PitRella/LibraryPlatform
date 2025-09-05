from typing import Any, final

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository
from src.books.exceptions import ForgottenParametersException


class BaseService:
    """Base service class for business logic layers.

    Provides common functionality for services, including access to the
    repository and database session.

    Attributes:
        _session (AsyncSession): SQLAlchemy asynchronous session.
        _repo (BaseRepository): Repository instance for database operations.

    """

    def __init__(self, db_session: AsyncSession, repo: BaseRepository) -> None:
        """Initialize the service with a database session and repository.

        Args:
            db_session (AsyncSession): Asynchronous database session.
            repo (BaseRepository): Repository instance for CRUD operations.

        """
        self._session: AsyncSession = db_session
        self._repo: BaseRepository = repo

    @staticmethod
    @final
    def _validate_schema_for_update_request(
        schema: BaseModel,
    ) -> dict[str, Any]:
        """Validate that a Pydantic update schema contains at least one field.

        This method removes unset and None values from the schema.
        Raises ForgottenParametersException if no fields are provided.

        Args:
            schema (BaseModel): Pydantic schema instance for update.

        Returns:
            dict[str, Any]: Dictionary of fields to update.

        Raises:
            ForgottenParametersException: If the schema has no fields to update.

        """
        schema_fields: dict[str, str] = schema.model_dump(
            exclude_none=True,
            exclude_unset=True,
        )  # Delete None key value pair
        if not schema_fields:
            raise ForgottenParametersException
        return schema_fields
