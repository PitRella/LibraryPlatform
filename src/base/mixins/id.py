from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class PrimaryKeyMixin(Base):
    """Mixin class to add an auto-incrementing primary key `id` column.

    This class is intended to be used as a base for SQLAlchemy models.
    It is marked as abstract and does not create its own table.

    Attributes:
        id (Mapped[int]): Auto-incrementing primary key column.

    """

    __abstract__ = True
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )
