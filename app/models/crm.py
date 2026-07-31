from __future__ import annotations

from datetime import datetime, timezone
from sqlalchemy import String, Integer, Float, Boolean, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class PipelineStage(Base):
    __tablename__ = "pipeline_stages"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    stage_order: Mapped[int] = mapped_column(Integer, default=0)
    color: Mapped[str] = mapped_column(String(30), default="#1769e8")
    sla_inactivity_days: Mapped[int] = mapped_column(Integer, default=3)
    win_probability_pct: Mapped[float] = mapped_column(Float, default=20.0)

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    size_range: Mapped[str | None] = mapped_column(String(50), nullable=True)
    annual_revenue: Mapped[float | None] = mapped_column(Float, nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    website: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class Contact(Base):
    __tablename__ = "contacts"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    company_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    position: Mapped[str | None] = mapped_column(String(100), nullable=True)
    is_decision_maker: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class Lead(Base):
    __tablename__ = "leads"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    value_mxn: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String(50), default="NEW") # NEW, QUALIFIED, UNQUALIFIED
    source: Mapped[str] = mapped_column(String(50), default="MANUAL") # APIFY, WEB, MANUAL
    score: Mapped[int] = mapped_column(Integer, default=50)
    temperature: Mapped[str] = mapped_column(String(20), default="WARM") # HOT, WARM, COLD
    raw_data_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class Deal(Base):
    __tablename__ = "deals"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    lead_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    company_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    stage_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    company: Mapped[str] = mapped_column(String(255), nullable=False)
    value: Mapped[float] = mapped_column(Float, default=0.0)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    score: Mapped[int] = mapped_column(Integer, default=70)
    inactivity: Mapped[str] = mapped_column(String(50), default="Hoy")
    inactivity_days: Mapped[int] = mapped_column(Integer, default=0)
    risk: Mapped[bool] = mapped_column(Boolean, default=False)
    last_interaction_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    deal_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    activity_type: Mapped[str] = mapped_column(String(50), default="CALL") # CALL, EMAIL, MEETING, TASK
    due_date: Mapped[str] = mapped_column(String(50), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))

class FollowUp(Base):
    __tablename__ = "followups"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    deal_id: Mapped[str] = mapped_column(String(64), nullable=False)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    channel: Mapped[str] = mapped_column(String(50), default="WHATSAPP")
    status: Mapped[str] = mapped_column(String(50), default="PENDING") # PENDING, APPROVED, SENT, BLOCKED
    scheduled_at: Mapped[str] = mapped_column(String(50), nullable=False)
    message_draft: Mapped[str] = mapped_column(Text, nullable=False)
    approval_mode: Mapped[str] = mapped_column(String(50), default="REQUIRE_APPROVAL")

class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    sku: Mapped[str] = mapped_column(String(100), nullable=False)
    price_mxn: Mapped[float] = mapped_column(Float, default=0.0)
    category: Mapped[str] = mapped_column(String(100), default="Consultoría")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
