from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class Interaction(Base):
    __tablename__ = "interactions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    deal_id: Mapped[str] = mapped_column(String(64), nullable=False)
    interaction_type: Mapped[str] = mapped_column(String(50), nullable=False) # CALL_AUDIO, CALL_TRANSCRIPT, WHATSAPP, EMAIL
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class CallAnalysis(Base):
    __tablename__ = "call_analyses"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    interaction_id: Mapped[str] = mapped_column(String(64), nullable=False)
    deal_id: Mapped[str] = mapped_column(String(64), nullable=False)
    duration_seconds: Mapped[int] = mapped_column(Integer, default=0)
    talk_listen_ratio: Mapped[float] = mapped_column(Float, default=0.5) # e.g. 0.42 = rep talked 42%
    silence_seconds: Mapped[int] = mapped_column(Integer, default=0)
    turn_count: Mapped[int] = mapped_column(Integer, default=0)
    score_1_to_10: Mapped[float] = mapped_column(Float, default=7.5)
    coaching_summary: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
