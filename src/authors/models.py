from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.base.mixins import PrimaryKeyMixin, TimeStampMixin
from src.books.models import Book


class Author(PrimaryKeyMixin, TimeStampMixin):
    """Author model for storing author information."""

    __tablename__ = 'authors'
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True,
        index=True,
    )
    password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    biography: Mapped[str | None] = mapped_column(Text, nullable=True)
    birth_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    nationality: Mapped[str | None] = mapped_column(String(100), nullable=True)
    books: Mapped[list['Book']] = relationship(
        'Book', back_populates='author', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f'<Author(id={self.id}, name="{self.name}")>'
