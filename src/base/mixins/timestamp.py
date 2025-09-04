from datetime import datetime

from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class TimeStampMixin(Base):
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

