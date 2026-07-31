from __future__ import annotations

from pydantic import BaseModel
from typing import Any

class DealCreate(BaseModel):
    company: str
    value: float
    owner: str = "Alejandro Ruiz"
    stage_id: str = "new"
    email: str | None = None
    phone: str | None = None

class DealUpdateStage(BaseModel):
    stage_id: str

class DealOut(BaseModel):
    id: str
    company: str
    value: float
    owner: str
    score: int
    inactivity: str
    inactivity_days: int
    risk: bool
    stage_id: str
    created_at: str

class StageOut(BaseModel):
    id: str
    title: str
    color: str
    deals: list[DealOut] = []

class LeadCreate(BaseModel):
    company_name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    value_mxn: float = 0.0
    industry: str | None = None
    size_range: str | None = None
    annual_revenue: float | None = None

class LeadOut(BaseModel):
    id: str
    company_name: str
    contact_name: str | None = None
    email: str | None = None
    phone: str | None = None
    value_mxn: float
    status: str
    source: str
    score: int
    temperature: str

class CompanyOut(BaseModel):
    id: str
    name: str
    industry: str | None = None
    size_range: str | None = None
    annual_revenue: float | None = None
    phone: str | None = None
    website: str | None = None
    location: str | None = None

class ContactOut(BaseModel):
    id: str
    company_id: str | None = None
    first_name: str
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    position: str | None = None

class ActivityCreate(BaseModel):
    title: str
    activity_type: str = "CALL"
    due_date: str = "Hoy"
    deal_id: str | None = None

class ActivityOut(BaseModel):
    id: str
    title: str
    activity_type: str
    due_date: str
    completed: bool

class FollowUpOut(BaseModel):
    id: str
    company_name: str
    channel: str
    status: str
    scheduled_at: str
    message_draft: str
    approval_mode: str

class ProductOut(BaseModel):
    id: str
    name: str
    sku: str
    price_mxn: float
    category: str
    description: str | None = None
