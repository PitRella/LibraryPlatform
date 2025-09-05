from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import ListableRepository


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
        conditions = ' AND '.join(f'{key} = :{key}' for key in filters)

        sql = text(f"""
            SELECT id, title, genre, language, published_year, author_id, created_at
            FROM books
            WHERE {conditions}
            LIMIT 1
        """)

        async with self._session.begin():
            result = await self._session.execute(sql, filters)
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
        set_expr = ', '.join(f'{k} = :set_{k}' for k in update_data)
        conditions = ' AND '.join(f'{k} = :{k}' for k in filters)
        params = {**{f'set_{k}': v for k, v in update_data.items()}, **filters}

        sql = text(f"""
            UPDATE books
            SET {set_expr}
            WHERE {conditions}
            RETURNING *
        """)
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            row = result.mappings().first()
            return dict(row) if row else None

    async def delete_object(self, **filters: Any) -> None:
        """Delete a book matching the given filters.

        Args:
            **filters (Any): Column-value filters to identify the book.

        """
        conditions = ' AND '.join(f'{k} = :{k}' for k in filters)

        sql = text(f"""
            DELETE FROM books
            WHERE {conditions}
        """)

        async with self._session.begin():
            await self._session.execute(sql, filters)

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
        where_clause = ' AND '.join(filters) if filters else 'TRUE'
        sql = text(f"""
            SELECT id,
                   title,
                   genre,
                   language,
                   published_year,
                   author_id,
                   created_at
            FROM books
            WHERE {where_clause}
            ORDER BY id
            LIMIT :limit
        """)

        result = await self._session.execute(sql, params)
        rows = result.mappings().all()
        return [dict(r) for r in rows]
