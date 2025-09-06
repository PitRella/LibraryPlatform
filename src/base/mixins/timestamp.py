from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TimeStampMixin(Base):
    """Mixin class to add automatic timestamp columns to a SQLAlchemy model.

    This class is intended as an abstract base for other models.
    It provides `created_at` and `updated_at` columns that are automatically
    set and updated.

    Attributes:
        created_at (Mapped[datetime]): Timestamp when the record was created.
            Defaults to the current database time.
        updated_at (Mapped[datetime]): Timestamp when the record was last
            updated. Automatically updated on any record modification.

    """

    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
