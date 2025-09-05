from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthorRepository(BaseRepository):
    """Repository for performing CRUD operations on the `authors` table.

    Inherits from BaseRepository. Provides asynchronous methods to
    create, retrieve, update, and delete author records.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session (AsyncSession): Asynchronous SQLAlchemy session.

        """
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
        """Create a new author record in the database.

        Args:
            params (dict[str, Any]): Dictionary containing author fields:
                email, password, name, biography, birth_year, nationality,
                created_at.

        Returns:
            int: ID of the newly created author.

        """
        sql = text(
            """
            INSERT INTO authors (email, password, name, biography,
                                 birth_year, nationality, created_at)
            VALUES (:email, :password, :name, :biography, :birth_year,
                    :nationality, :created_at)
            RETURNING id
            """
        )
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            return cast(int, result.scalar_one())

    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        """Retrieve a single author record matching the given filters.

        Args:
            **filters (Any): Keyword arguments for filtering the query.

        Returns:
            dict[str, Any] | None: Dictionary of author fields if found,
            otherwise None.

        """
        conditions = ' AND '.join(f'{key} = :{key}' for key in filters)

        sql = text(f"""
            SELECT id, email, name, biography, birth_year, nationality, created_at, password
            FROM authors
            WHERE {conditions}
            LIMIT 1
        """)

        async with self._session.begin():
            result = await self._session.execute(sql, filters)
            row = result.mappings().first()
            return dict(row) if row else None

    async def delete_object(self, **filters: Any) -> None:
        """Deleting authors is not implemented.

        Raises:
            NotImplementedError: Always raised.

        """
        raise NotImplementedError

    async def update_object(
        self,
        update_data: dict[str, Any],
        **filters: Any,
    ) -> dict[str, Any] | None:
        """Updating authors is not implemented.

        Args:
            update_data (dict[str, Any]): Fields to update.
            **filters (Any): Filter criteria.

        Raises:
            NotImplementedError: Always raised.

        """
        raise NotImplementedError
