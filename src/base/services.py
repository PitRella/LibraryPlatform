from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:

    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        self._session: AsyncSession = db_session
