from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all RDRS database models."""


class Event(Base):
    """Persisted filesystem event."""

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    event_type: Mapped[str] = mapped_column(String(32), nullable=False, index=True)
    path: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    extension: Mapped[str] = mapped_column(String(32), default="", nullable=False)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    entropy: Mapped[float | None] = mapped_column(Float, nullable=True)
    suspicious: Mapped[bool] = mapped_column(default=False, nullable=False)
