from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class BaseService:

    def __init__(
            self,
            db_session: AsyncSession,
            repo: BaseRepository | None = None,
    ) -> None:
        self._session: AsyncSession = db_session
        self._repo: BaseRepository = repo or BaseRepository(self._session)
