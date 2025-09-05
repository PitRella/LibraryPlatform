from typing import Any, cast

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class AuthRepository(BaseRepository):
    """Repository for managing refresh tokens in the database."""

    def __init__(self, session: AsyncSession):
        """Initialize the repository with an async database session.

        Args:
            session (AsyncSession): SQLAlchemy async session.

        """
        super().__init__(session)

    async def create_object(self, params: dict[str, Any]) -> int:
        """Create a new refresh token record.

        Args:
            params (dict[str, Any]): Dictionary containing author_id,
                refresh_token, and expires_in.

        Returns:
            int: ID of the newly created refresh token.

        """
        sql = text("""
                   INSERT INTO refresh_tokens (author_id, refresh_token,
                                               expires_in, created_at)
                   VALUES (:author_id, :refresh_token, :expires_in, NOW())
                   RETURNING id
                   """)
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            return cast(int, result.scalar_one())

    async def get_object(self, **filters: Any) -> dict[str, Any] | None:
        """Retrieve a refresh token record matching the given filters.

        Args:
            **filters: Arbitrary column filters as key=value pairs.

        Returns:
            dict[str, Any] | None: Refresh token record if found,
                otherwise None.

        """
        conditions = ' AND '.join(f'{key} = :{key}' for key in filters)

        sql = text(f"""
                    SELECT id, author_id, refresh_token, expires_in, created_at
                    FROM refresh_tokens
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
        """Update a refresh token record matching filters with new data.

        Args:
            update_data (dict[str, Any]): Fields to update with values.
            **filters: Column filters to locate the record.

        Returns:
            dict[str, Any] | None: Updated record if found, otherwise None.

        """
        set_expr = ', '.join(f'{k} = :set_{k}' for k in update_data)
        conditions = ' AND '.join(f'{k} = :{k}' for k in filters)

        params = {**{f'set_{k}': v for k, v in update_data.items()}, **filters}

        sql = text(f"""
            UPDATE refresh_tokens
            SET {set_expr}
            WHERE {conditions}
            RETURNING *
        """)
        async with self._session.begin():
            result = await self._session.execute(sql, params)
            row = result.mappings().first()
            return dict(row) if row else None

    async def delete_object(self, **filters: Any) -> None:
        """Delete a token matching the given filters.

        Args:
            **filters (Any): Column-value filters to identify the token.

        """
        conditions = ' AND '.join(f'{k} = :{k}' for k in filters)

        sql = text(f"""
            DELETE FROM refresh_tokens
            WHERE {conditions}
        """)

        async with self._session.begin():
            await self._session.execute(sql, filters)
