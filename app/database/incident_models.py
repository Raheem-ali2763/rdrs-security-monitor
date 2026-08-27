from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models import Base


class Incident(Base):
    """Security incident detected by RDRS."""

    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        nullable=False,
        index=True,
    )
    severity: Mapped[str] = mapped_column(
        String(16),
        default="normal",
        nullable=False,
        index=True,
    )
    threat_score: Mapped[float] = mapped_column(
        Float,
        default=0.0,
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(16),
        default="open",
        nullable=False,
        index=True,
    )
    summary: Mapped[str] = mapped_column(
        Text,
        default="",
        nullable=False,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        index=True,
    )
    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    evidence: Mapped[list["Evidence"]] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
    )


class Evidence(Base):
    """Evidence associated with a security incident."""

    __tablename__ = "evidence"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    incident_id: Mapped[int] = mapped_column(
        ForeignKey("incidents.id"),
        nullable=False,
        index=True,
    )
    path: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_type: Mapped[str] = mapped_column(
        String(32),
        default="file",
        nullable=False,
    )
    sha256: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True,
    )
    collected_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    incident: Mapped[Incident] = relationship(
        back_populates="evidence",
    )
