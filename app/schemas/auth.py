from __future__ import annotations

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    full_name: str
    role: str
    tenant_id: str

class LoginRequest(BaseModel):
    email: str
    password: str

class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    role: str = "SALES_REP"

class UserOut(BaseModel):
    id: str
    tenant_id: str
    email: str
    full_name: str
    role: str
    avatar_url: str | None = None
