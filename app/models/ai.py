from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class AIRun(Base):
    __tablename__ = "ai_runs"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    agent_name: Mapped[str] = mapped_column(String(100), nullable=False) # Agent1_Prospector, Agent2_SuperSales, Agent3_FollowUp
    prompt_version: Mapped[str] = mapped_column(String(50), default="v1.0.0")
    latency_ms: Mapped[int] = mapped_column(Integer, default=120)
    tokens_used: Mapped[int] = mapped_column(Integer, default=350)
    cost_usd: Mapped[float] = mapped_column(Float, default=0.002)
    output_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
