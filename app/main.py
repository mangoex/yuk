from __future__ import annotations

import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Final

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.staticfiles import StaticFiles

from app import __version__
from app.core.database import AsyncSessionLocal
from app.core.init_db import init_db
from app.api.v1.auth import router as auth_router
from app.api.v1.deals import router as deals_router
from app.api.v1.leads import router as leads_router
from app.api.v1.companies import router as companies_router
from app.api.v1.contacts import router as contacts_router
from app.api.v1.activities import router as activities_router
from app.api.v1.followups import router as followups_router
from app.api.v1.prospecting import router as prospecting_router
from app.api.v1.calls import router as calls_router
from app.api.v1.reports import router as reports_router

SERVICE_NAME: Final = "antigravity-crm-api"
PROJECT_ROOT: Final = Path(__file__).resolve().parents[1]

class ServiceInfo(BaseModel):
    name: str
    version: str
    environment: str
    status: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables and seed data
    async with AsyncSessionLocal() as session:
        await init_db(session)
    yield

def create_app() -> FastAPI:
    environment = os.getenv("APP_ENV", "development")
    application = FastAPI(
        title="CRM Inteligente Antigravity",
        summary="API del CRM y sus agentes autónomos de IA.",
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # CORS configuration
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register API v1 Routers
    api_prefix = "/api/v1"
    application.include_router(auth_router, prefix=api_prefix)
    application.include_router(deals_router, prefix=api_prefix)
    application.include_router(leads_router, prefix=api_prefix)
    application.include_router(companies_router, prefix=api_prefix)
    application.include_router(contacts_router, prefix=api_prefix)
    application.include_router(activities_router, prefix=api_prefix)
    application.include_router(followups_router, prefix=api_prefix)
    application.include_router(prospecting_router, prefix=api_prefix)
    application.include_router(calls_router, prefix=api_prefix)
    application.include_router(reports_router, prefix=api_prefix)

    @application.get("/api/v1/system", response_model=ServiceInfo, tags=["system"])
    async def service_info() -> ServiceInfo:
        return ServiceInfo(
            name=SERVICE_NAME,
            version=__version__,
            environment=environment,
            status="ok",
        )

    @application.get("/health/live", tags=["health"])
    async def liveness() -> dict[str, str]:
        return {"status": "alive"}

    @application.get("/health/ready", tags=["health"])
    async def readiness() -> dict[str, str]:
        return {"status": "ready"}

    static_dir = Path(__file__).resolve().parent / "static"
    local_frontend_dist = PROJECT_ROOT / "frontend" / "dist" / "client"
    if not static_dir.exists() and local_frontend_dist.exists():
        static_dir = local_frontend_dist

    if static_dir.exists():
        application.mount("/", StaticFiles(directory=static_dir, html=True), name="frontend")

    return application

app = create_app()
