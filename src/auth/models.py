import uuid
from datetime import datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from src.base.mixins import PrimaryKeyMixin


class RefreshToken(PrimaryKeyMixin):
    """Model representing a refresh token for author authentication.

    Attributes:
        refresh_token (uuid.UUID): Unique UUID used as the refresh token.
        expires_in (float): Expiration time of the refresh token in seconds.
        created_at (datetime): Timestamp when the refresh token was created.
        author_id (int): ID of the author to whom this token belongs.

    """

    __tablename__ = 'refresh_tokens'

    refresh_token: Mapped[uuid.UUID] = mapped_column(
        UUID, index=True, comment='Refresh token UUID'
    )
    expires_in: Mapped[float] = mapped_column(
        nullable=False, comment='Refresh token expiration time in seconds'
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        comment='Refresh token creation time',
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id', ondelete='CASCADE'), comment='Author ID'
    )

    def __repr__(self) -> str:
        """Return a string representation of the RefreshToken instance."""
        return (
            f'<RefreshToken(id={self.id}, author_id={self.author_id}, '
            f'refresh_token={self.refresh_token},'
            f' expires_in={self.expires_in})>'
        )
