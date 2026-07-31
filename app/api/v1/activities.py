from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Activity
from app.schemas.crm import ActivityCreate, ActivityOut

router = APIRouter(prefix="/activities", tags=["activities"])

@router.get("", response_model=list[ActivityOut])
async def list_activities(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    res = await db.execute(select(Activity).where(Activity.tenant_id == tenant_id))
    activities = res.scalars().all()
    return [
        ActivityOut(
            id=a.id,
            title=a.title,
            activity_type=a.activity_type,
            due_date=a.due_date,
            completed=a.completed,
        )
        for a in activities
    ]

@router.post("", response_model=ActivityOut)
async def create_activity(
    req: ActivityCreate,
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    activity_id = str(uuid.uuid4())[:8]
    act = Activity(
        id=activity_id,
        tenant_id=tenant_id,
        deal_id=req.deal_id,
        title=req.title,
        activity_type=req.activity_type,
        due_date=req.due_date,
        completed=False,
    )
    db.add(act)
    await db.commit()
    await db.refresh(act)
    return ActivityOut(
        id=act.id,
        title=act.title,
        activity_type=act.activity_type,
        due_date=act.due_date,
        completed=act.completed,
    )
