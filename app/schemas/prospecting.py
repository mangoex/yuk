from __future__ import annotations

from pydantic import BaseModel
from typing import Any

class ApifyRunRequest(BaseModel):
    search_query: str
    location: str = "México"
    limit_count: int = 5

class ApifyRunOut(BaseModel):
    status: str
    search_query: str
    location: str
    items_scraped: int
    leads: list[dict[str, Any]] = []
