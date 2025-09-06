from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.query_builder import SecureQueryBuilder
from src.base.repositories import ListableRepository
from src.books.exceptions import (
    NoFiltersException,
    NoUpdateDataException,
    UnsafeFilterException,
)


class BookRepository(ListableRepository):
    """Repository for performing CRUD operations on books.

    Provides methods to create, retrieve, update, delete, and list books
    using raw SQL queries with SQLAlchemy AsyncSession.

    Attributes:
        _session (AsyncSession): Async database session for operations.

    """

    def __init__(self, session: AsyncSession):
        """Initialize the repository with a database session.

        Args:
            session (AsyncSession): Async session to interact with the DB.

        """
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
        """Insert a new book into the database.

        Args:
            params (dict[str, Any]): Book fields (title, genre, language,
                                     published_year, author_id, created_at).

        Returns:
            int: ID of the newly created book.

        """
        sql = text(
            """
            INSERT INTO books (title, genre, language, published_year,
                               author_id, created_at)
            VALUES (:title, :genre, :language, :published_year, :author_id,
                    :created_at)
            RETURNING id
            """
        )
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            return cast(int, result.scalar_one())

    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        """Retrieve a single book matching the given filters.

        Args:
            **filters (Any): Column-value filters for the query.

        Returns:
            dict[str, Any] | None: Book data if found, else None.

        """
        if not filters:
            return None

        # Build safe WHERE clause using SecureQueryBuilder
        conditions = [(key, '=', key) for key in filters]
        where_clause, safe_params = SecureQueryBuilder.build_where_clause(
            'books', conditions, filters
        )

        sql = text(
            'SELECT id, title, genre, language, published_year, '
            'author_id, created_at '
            'FROM books '
            'WHERE ' + where_clause + ' '
            'LIMIT 1'
        )

        async with self._session.begin():
            result = await self._session.execute(sql, safe_params)
            row = result.mappings().first()
            return dict(row) if row else None

    async def update_object(
        self,
        update_data: dict[str, Any],
        **filters: Any,
    ) -> dict[str, Any] | None:
        """Update fields of a book matching the filters.

        Args:
            update_data (dict[str, Any]): Fields to update.
            **filters (Any): Column-value filters to identify the book.

        Returns:
            dict[str, Any] | None: Updated book data if found, else None.

        """
        if not update_data:
            raise NoUpdateDataException
        if not filters:
            raise NoFiltersException

        # Build safe SET clause
        set_clause, set_params = SecureQueryBuilder.build_set_clause(
            'books',
            list(update_data.keys()),
            {f'set_{k}': v for k, v in update_data.items()},
        )

        # Build safe WHERE clause
        where_conditions = [(key, '=', key) for key in filters]
        where_clause, where_params = SecureQueryBuilder.build_where_clause(
            'books', where_conditions, filters
        )

        # Combine parameters
        params = {**set_params, **where_params}

        sql = text(
            'UPDATE books '
            'SET ' + set_clause + ' '
            'WHERE ' + where_clause + ' '
            'RETURNING *'
        )
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            row = result.mappings().first()
            return dict(row) if row else None

    async def delete_object(self, **filters: Any) -> None:
        """Delete a book matching the given filters.

        Args:
            **filters (Any): Column-value filters to identify the book.

        """
        if not filters:
            raise NoFiltersException

        # Build safe WHERE clause
        where_conditions = [(key, '=', key) for key in filters]
        where_clause, safe_params = SecureQueryBuilder.build_where_clause(
            'books', where_conditions, filters
        )

        # where_clause is validated by SecureQueryBuilder, so this is safe
        sql = text('DELETE FROM books WHERE ' + where_clause)  # noqa: S608

        async with self._session.begin():
            await self._session.execute(sql, safe_params)

    async def list_objects(
        self,
        filters: list[str],
        params: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """List books matching optional filter conditions.

        Args:
            filters (list[str]): List of SQL conditions for WHERE clause.
            params (dict[str, Any]): Parameters for SQL query.

        Returns:
            list[dict[str, Any]]: List of books matching filters.

        """
        # For list_objects, we need to validate that filters contain only safe
        # conditions. This is a more complex case as we need to parse the filter
        # strings. For now, we'll use a simple approach that validates against
        # known patterns

        if not filters:
            where_clause = 'TRUE'
        else:
            validated_filters = []
            for filter_str in filters:
                if not self._is_safe_filter(filter_str):
                    raise UnsafeFilterException(filter_str)
                validated_filters.append(filter_str)
            where_clause = ' AND '.join(validated_filters)

        sql = text(
            'SELECT id, title, genre, language, published_year, '
            'author_id, created_at '
            'FROM books '
            'WHERE ' + where_clause + ' '
            'ORDER BY id '
            'LIMIT :limit'
        )

        result = await self._session.execute(sql, params)
        rows = result.mappings().all()
        return [dict(r) for r in rows]

    def _is_safe_filter(self, filter_str: str) -> bool:
        """Check if a filter string is safe to use.

        Args:
            filter_str (str): Filter string to validate.

        Returns:
            bool: True if safe, False otherwise.

        """
        # Basic validation - check for common SQL injection patterns
        dangerous_patterns = [
            ';',
            '--',
            '/*',
            '*/',
            'xp_',
            'sp_',
            'exec',
            'execute',
            'union',
            'select',
            'insert',
            'update',
            'delete',
            'drop',
            'create',
            'alter',
            'grant',
            'revoke',
        ]

        filter_lower = filter_str.lower()
        for pattern in dangerous_patterns:
            if pattern in filter_lower:
                return False

        # Check that it contains only allowed column names
        allowed_columns = SecureQueryBuilder.ALLOWED_COLUMNS['books']
        words = (
            filter_str.replace('=', ' ')
            .replace('!=', ' ')
            .replace('<', ' ')
            .replace('>', ' ')
            .split()
        )

        for word in words:
            if (
                word.isalpha()
                and word not in allowed_columns
                and word.upper() not in ['AND', 'OR', 'NOT', 'IN', 'LIKE']
            ):
                return False

        return True
