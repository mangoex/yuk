from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Lead
from app.schemas.prospecting import ApifyRunRequest, ApifyRunOut
from app.services.apify_service import apify_service

router = APIRouter(prefix="/prospecting", tags=["prospecting"])

@router.post("/run", response_model=ApifyRunOut)
async def run_apify_prospecting(
    req: ApifyRunRequest,
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    result = await apify_service.run_prospecting_scrape(
        search_query=req.search_query,
        location=req.location,
        limit_count=req.limit_count,
    )

    imported_leads = []
    for lead_data in result.get("leads", []):
        lead_id = str(uuid.uuid4())[:8]
        lead = Lead(
            id=lead_id,
            tenant_id=tenant_id,
            company_name=lead_data["company_name"],
            contact_name=lead_data["contact_name"],
            email=lead_data["email"],
            phone=lead_data["phone"],
            value_mxn=lead_data["annual_revenue"] * 0.1,
            status="NEW",
            source="APIFY",
            score=lead_data["score"],
            temperature=lead_data["temperature"],
        )
        db.add(lead)
        imported_leads.append(lead_data)

    await db.commit()

    return ApifyRunOut(
        status=result["status"],
        search_query=req.search_query,
        location=req.location,
        items_scraped=len(imported_leads),
        leads=imported_leads,
    )
