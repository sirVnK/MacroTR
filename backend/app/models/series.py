from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    evds_code: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(220))
    description: Mapped[str] = mapped_column(Text)
    source: Mapped[str] = mapped_column(String(120), default="TCMB EVDS")
    frequency: Mapped[str] = mapped_column(String(32))
    unit: Mapped[str] = mapped_column(String(64))
    category: Mapped[str] = mapped_column(String(96), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_updated: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_successful_fetch: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_fetch_attempt: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    fetch_status: Mapped[str] = mapped_column(String(32), default="not_fetched")
    fetch_error: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    observations = relationship(
        "Observation",
        back_populates="series",
        cascade="all, delete-orphan",
    )
