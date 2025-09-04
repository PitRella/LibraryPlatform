from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class PrimaryKeyMixin(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

