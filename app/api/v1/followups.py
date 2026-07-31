from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import FollowUp
from app.schemas.crm import FollowUpOut

router = APIRouter(prefix="/followups", tags=["followups"])

@router.get("", response_model=list[FollowUpOut])
async def list_followups(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(FollowUp).where(FollowUp.tenant_id == tenant_id))
    items = res.scalars().all()
    return [
        FollowUpOut(
            id=f.id,
            company_name=f.company_name,
            channel=f.channel,
            status=f.status,
            scheduled_at=f.scheduled_at,
            message_draft=f.message_draft,
            approval_mode=f.approval_mode,
        )
        for f in items
    ]
