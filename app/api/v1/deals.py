from __future__ import annotations

import uuid
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_current_user, get_tenant_id
from app.models.user import User
from app.models.crm import PipelineStage, Deal
from app.schemas.crm import DealCreate, DealOut, DealUpdateStage, StageOut

router = APIRouter(prefix="/deals", tags=["deals"])

@router.get("/stages", response_model=list[StageOut])
async def get_pipeline_stages_with_deals(
    query: str | None = Query(default=None),
    risk_only: bool = Query(default=False),
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    # Fetch stages ordered
    stages_res = await db.execute(
        select(PipelineStage)
        .where(PipelineStage.tenant_id == tenant_id)
        .order_by(PipelineStage.stage_order)
    )
    stages = stages_res.scalars().all()

    # Fetch deals for tenant
    deals_query = select(Deal).where(Deal.tenant_id == tenant_id)
    if risk_only:
        deals_query = deals_query.where(Deal.risk == True)
    
    deals_res = await db.execute(deals_query)
    all_deals = deals_res.scalars().all()

    if query:
        q_lower = query.lower()
        all_deals = [d for d in all_deals if q_lower in d.company.lower() or q_lower in d.owner.lower()]

    # Group deals by stage
    result = []
    for stage in stages:
        stage_deals = [d for d in all_deals if d.stage_id == stage.id]
        deal_outs = [
            DealOut(
                id=d.id,
                company=d.company,
                value=d.value,
                owner=d.owner,
                score=d.score,
                inactivity=d.inactivity,
                inactivity_days=d.inactivity_days,
                risk=d.risk,
                stage_id=d.stage_id,
                created_at=d.created_at.isoformat(),
            )
            for d in stage_deals
        ]
        result.append(
            StageOut(
                id=stage.id,
                title=stage.title,
                color=stage.color,
                deals=deal_outs,
            )
        )
    return result

@router.post("", response_model=DealOut)
async def create_deal(
    req: DealCreate,
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    deal_id = str(uuid.uuid4())[:8]
    new_deal = Deal(
        id=deal_id,
        tenant_id=tenant_id,
        stage_id=req.stage_id,
        company=req.company,
        value=req.value,
        owner=req.owner or current_user.full_name,
        score=68,
        inactivity="Hoy",
        inactivity_days=0,
        risk=False,
    )
    db.add(new_deal)
    await db.commit()
    await db.refresh(new_deal)

    return DealOut(
        id=new_deal.id,
        company=new_deal.company,
        value=new_deal.value,
        owner=new_deal.owner,
        score=new_deal.score,
        inactivity=new_deal.inactivity,
        inactivity_days=new_deal.inactivity_days,
        risk=new_deal.risk,
        stage_id=new_deal.stage_id,
        created_at=new_deal.created_at.isoformat(),
    )

@router.patch("/{deal_id}/stage", response_model=DealOut)
async def update_deal_stage(
    deal_id: str,
    req: DealUpdateStage,
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Deal).where(Deal.id == deal_id, Deal.tenant_id == tenant_id)
    )
    deal = result.scalars().first()
    if not deal:
        raise HTTPException(status_code=404, detail="Oportunidad no encontrada")

    deal.stage_id = req.stage_id
    await db.commit()
    await db.refresh(deal)

    return DealOut(
        id=deal.id,
        company=deal.company,
        value=deal.value,
        owner=deal.owner,
        score=deal.score,
        inactivity=deal.inactivity,
        inactivity_days=deal.inactivity_days,
        risk=deal.risk,
        stage_id=deal.stage_id,
        created_at=deal.created_at.isoformat(),
    )
