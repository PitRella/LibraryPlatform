import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.base.mixins import PrimaryKeyMixin


class RefreshToken(PrimaryKeyMixin):
    __tablename__ = 'refresh_tokens'

    refresh_token: Mapped[uuid.UUID] = mapped_column(
        UUID,
        index=True,
        comment='Refresh token UUID'
    )
    expires_in: Mapped[float] = mapped_column(
        nullable=False,
        comment='Refresh token expiration time in seconds'
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        comment='Refresh token creation time'
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id', ondelete='CASCADE'),
        comment='Author ID'
    )
