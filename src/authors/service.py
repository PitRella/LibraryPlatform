from datetime import UTC
from datetime import datetime as dt
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.services import Hasher
from src.authors.exceptions import AuthorNotFoundByIdException
from src.authors.repositories import AuthorRepository
from src.authors.schemas import CreateAuthorRequestSchema
from src.base.services import BaseService


class AuthorService(BaseService):
    """Service layer for author-related operations.

    Provides methods to create new authors and retrieve author
    information by ID.
    """

    def __init__(self, db_session: AsyncSession) -> None:
        """Initialize AuthorService with a database session.

        Args:
            db_session (AsyncSession): Asynchronous SQLAlchemy session.

        """
        super().__init__(db_session, repo=AuthorRepository(db_session))

    async def get_author_by_id(self, user_id: int | str) -> dict[str, Any]:
        """Retrieve author details by ID.

        Args:
            user_id (int | str): ID of the author to retrieve.

        Raises:
            AuthorNotFoundByIdException: If no author exists with the
                given ID.

        Returns:
            dict[str, Any]: Dictionary containing author fields.

        """
        author_data = await self._repo.get_object(id=int(user_id))
        if not author_data:
            raise AuthorNotFoundByIdException
        return author_data

    async def create_author(
        self, author_schema: CreateAuthorRequestSchema
    ) -> int:
        """Create a new author in the system.

        The password is hashed before storing in the database, and
        creation timestamp is set.

        Args:
            author_schema (CreateAuthorRequestSchema): Schema containing
                the details of the author to create.

        Returns:
            int: ID of the newly created author.

        """
        author_data = author_schema.model_dump()
        author_data['password'] = Hasher.hash_password(author_schema.password)
        author_data['created_at'] = dt.now(UTC)
        author_id: int = await self._repo.create_object(author_data)
        return author_id
