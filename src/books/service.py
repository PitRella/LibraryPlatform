
from src.base.services import BaseService
from sqlalchemy.ext.asyncio import AsyncSession

from src.books.repositories import BookRepository


class BooksService(BaseService):
    def __init__(
            self,
            db_session: AsyncSession
    ) -> None:
        super().__init__(db_session, repo=BookRepository(db_session))
