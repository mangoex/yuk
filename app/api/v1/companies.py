from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Company
from app.schemas.crm import CompanyOut

router = APIRouter(prefix="/companies", tags=["companies"])

@router.get("", response_model=list[CompanyOut])
async def list_companies(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Company).where(Company.tenant_id == tenant_id))
    companies = res.scalars().all()
    return [
        CompanyOut(
            id=c.id,
            name=c.name,
            industry=c.industry,
            size_range=c.size_range,
            annual_revenue=c.annual_revenue,
            phone=c.phone,
            website=c.website,
            location=c.location,
        )
        for c in companies
    ]
