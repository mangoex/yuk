from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.dependencies import get_tenant_id
from app.models.crm import Deal, PipelineStage
from app.services.calculations import calculate_weighted_forecast

router = APIRouter(prefix="/reports", tags=["reports"])

@router.get("/forecast")
async def get_weighted_forecast_report(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    deals_res = await db.execute(select(Deal).where(Deal.tenant_id == tenant_id))
    deals = deals_res.scalars().all()

    stages_res = await db.execute(select(PipelineStage).where(PipelineStage.tenant_id == tenant_id))

    # Map win probabilities
    stages_res = await db.execute(select(PipelineStage).where(PipelineStage.tenant_id == tenant_id))
    stages = stages_res.scalars().all()
    win_prob_map = {s.id: s.win_probability_pct for s in stages}

    deals_dicts = []
    for d in deals:
        deals_dicts.append({
            "value": d.value,
            "win_probability_pct": win_prob_map.get(d.stage_id, 25.0),
            "score": d.score,
        })

    forecast_result = calculate_weighted_forecast(deals_dicts)
    return forecast_result

@router.get("/stats")
async def get_crm_stats(
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
):
    deals_res = await db.execute(select(Deal).where(Deal.tenant_id == tenant_id))
    deals = deals_res.scalars().all()

    total_value = sum(d.value for d in deals)
    risk_count = sum(1 for d in deals if d.risk)
    avg_score = round(sum(d.score for d in deals) / len(deals), 1) if deals else 70.0

    return {
        "total_deals": len(deals),
        "total_pipeline_value_mxn": total_value,
        "deals_at_risk": risk_count,
        "average_lead_score": avg_score,
        "ai_agents_active": 3,
    }
