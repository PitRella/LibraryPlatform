from typing import TYPE_CHECKING

from sqlalchemy import Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.schema import ForeignKey

if TYPE_CHECKING:
    from src.authors.models import Author
from src.base.mixins import PrimaryKeyMixin, TimeStampMixin
from src.books.enum import BookGenre, BookLanguage


class Book(PrimaryKeyMixin, TimeStampMixin):
    """SQLAlchemy model for a book entity.

    Inherits primary key and timestamp mixins for ID and timestamps.

    Attributes:
        title (str): Title of the book, indexed for faster search.
        genre (BookGenre): Genre of the book as an Enum.
        language (BookLanguage): Language of the book as an Enum.
        published_year (int): Year the book was published.
        author_id (int): Foreign key referencing the author.
        author (Author): Relationship to the Author model.

    """

    __tablename__ = 'books'

    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    genre: Mapped[BookGenre] = mapped_column(
        Enum(BookGenre), nullable=False, index=True
    )
    language: Mapped[BookLanguage] = mapped_column(
        Enum(BookLanguage), nullable=False, index=True
    )
    published_year: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id', ondelete='CASCADE'), nullable=False, index=True
    )
    author: Mapped['Author'] = relationship('Author', back_populates='books')

    def __repr__(self) -> str:
        """Return a string representation of the book instance.

        Returns:
            str: Formatted string showing id, title, and author_id.

        """
        return f'<Book(id={self.id}, title="{self.title}", author_id={self.author_id})>'
