from sqlalchemy.ext.asyncio.session import AsyncSession

from src.auth.exceptions import WrongCredentialsException
from src.auth.repositories import AuthRepository
from src.auth.services import Hasher
from src.authors.models import Author
from src.authors.repositories import AuthorRepository
from src.base.repositories import BaseRepository
from src.base.services import BaseService


class AuthService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession,
            auth_repo: BaseRepository | None = None,
            author_repo: BaseRepository | None = None,
    ) -> None:
        super().__init__(db_session, repo=auth_repo or AuthRepository(db_session))
        self._author_repo = author_repo or AuthorRepository(db_session)

    @staticmethod
    def _verify_user_password(author: Author | None, password: str) -> None:
        if not author or not Hasher.verify_password(password, author.password):
            raise WrongCredentialsException

    async def auth_user(self, email: str, password: str) -> Author:
        author: Author | None = await self._author_repo.get_object(email=email)
        self._verify_user_password(author, password)
        return author
