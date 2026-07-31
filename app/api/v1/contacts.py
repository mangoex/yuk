from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Contact
from app.schemas.crm import ContactOut

router = APIRouter(prefix="/contacts", tags=["contacts"])

@router.get("", response_model=list[ContactOut])
async def list_contacts(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Contact).where(Contact.tenant_id == tenant_id))
    contacts = res.scalars().all()
    return [
        ContactOut(
            id=c.id,
            company_id=c.company_id,
            first_name=c.first_name,
            last_name=c.last_name,
            email=c.email,
            phone=c.phone,
            position=c.position,
        )
        for c in contacts
    ]
