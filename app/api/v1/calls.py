from __future__ import annotations

from typing import Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.services.agents.supersales import supersales_agent

router = APIRouter(prefix="/calls", tags=["calls"])

class CallAnalyzeRequest(BaseModel):
    company_name: str
    duration_seconds: int = 420
    turns: list[dict[str, Any]] | None = None

@router.post("/analyze")
async def analyze_sales_call(req: CallAnalyzeRequest):
    result = supersales_agent.analyze_call(
        company_name=req.company_name,
        turns=req.turns,
        duration_seconds=req.duration_seconds,
    )
    return result
