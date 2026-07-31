from __future__ import annotations

import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from jose import jwt

from app.core.config import settings

def get_password_hash(password: str) -> str:
    """Hash password using standard library pbkdf2_hmac sha256."""
    salt = hashlib.sha256(settings.SECRET_KEY.encode()).digest()[:16]
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return key.hex()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return get_password_hash(plain_password) == hashed_password

def create_access_token(subject: str | Any, tenant_id: str, role: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "tenant_id": tenant_id,
        "role": role,
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
