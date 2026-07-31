from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Lead
from app.schemas.crm import LeadCreate, LeadOut
from app.services.agents.prospector import prospector_agent

router = APIRouter(prefix="/leads", tags=["leads"])

@router.get("", response_model=list[LeadOut])
async def list_leads(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Lead).where(Lead.tenant_id == tenant_id))
    leads = res.scalars().all()
    return [
        LeadOut(
            id=l.id,
            company_name=l.company_name,
            contact_name=l.contact_name,
            email=l.email,
            phone=l.phone,
            value_mxn=l.value_mxn,
            status=l.status,
            source=l.source,
            score=l.score,
            temperature=l.temperature,
        )
        for l in leads
    ]

@router.post("", response_model=LeadOut)
async def create_lead(
    req: LeadCreate,
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    # Run Agent 1 (Prospector) Qualification
    qual = prospector_agent.qualify_lead({
        "company_name": req.company_name,
        "industry": req.industry,
        "size_range": req.size_range,
        "annual_revenue": req.annual_revenue,
    })

    lead_id = str(uuid.uuid4())[:8]
    lead = Lead(
        id=lead_id,
        tenant_id=tenant_id,
        company_name=req.company_name,
        contact_name=req.contact_name,
        email=req.email,
        phone=req.phone,
        value_mxn=req.value_mxn,
        status="NEW",
        source="MANUAL",
        score=qual["score"],
        temperature=qual["temperature"],
    )
    db.add(lead)
    await db.commit()
    await db.refresh(lead)

    return LeadOut(
        id=lead.id,
        company_name=lead.company_name,
        contact_name=lead.contact_name,
        email=lead.email,
        phone=lead.phone,
        value_mxn=lead.value_mxn,
        status=lead.status,
        source=lead.source,
        score=lead.score,
        temperature=lead.temperature,
    )
