from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.repositories import AuthRepository
from src.base.services import BaseService


class AuthService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session, repo=AuthRepository(db_session))