from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.base.mixins import PrimaryKeyMixin, TimeStampMixin


class Author(PrimaryKeyMixin,TimeStampMixin):
    """Author model for storing author information."""

    __tablename__ = 'authors'

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    biography: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    birth_year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    nationality: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    def __repr__(self) -> str:
        return f'<Author(id={self.id}, name="{self.name}")>'
