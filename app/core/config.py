from __future__ import annotations

import os
from dataclasses import dataclass

@dataclass
class Settings:
    PROJECT_NAME: str = "Antigravity CRM"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-yuk-consultorpro-2026")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # DB fallback to SQLite aiosqlite for seamless local running, PostgreSQL when DATABASE_URL is set
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./crm_yuk.db")
    
    APIFY_API_TOKEN: str = os.getenv("APIFY_API_TOKEN", "")
    DEFAULT_TENANT_ID: str = "consultorpro-org"

settings = Settings()
