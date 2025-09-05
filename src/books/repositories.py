from typing import Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.base.repositories import BaseRepository


class BookRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
