from __future__ import annotations

from typing import Annotated
from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", auto_error=False)

async def get_tenant_id(x_tenant_id: str | None = Header(default=None)) -> str:
    """Extrae el tenant_id del header HTTP X-Tenant-ID o usa el predeterminado."""
    return x_tenant_id or settings.DEFAULT_TENANT_ID

async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    tenant_id: str = Depends(get_tenant_id),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Valida el token JWT y devuelve el usuario autenticado."""
    # Si no hay token en modo dev/demo, retornar un usuario demostrativo por defecto
    if not token:
        # Check if default user exists in DB
        result = await db.execute(select(User).where(User.tenant_id == tenant_id))
        user = result.scalars().first()
        if user:
            return user
        # Dynamic fallback user instance
        return User(
            id="user-demo-1",
            tenant_id=tenant_id,
            email="admin@consultorpro.es",
            password_hash="mock_hash",
            full_name="Alejandro Ruiz",
            role="TENANT_ADMIN",
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales de acceso",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub", "")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise credentials_exception
    return user

def require_role(allowed_roles: list[str]):
    """Decorator / Dependency para verificar el rol del usuario."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != "SUPER_ADMIN":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos suficientes para realizar esta acción",
            )
        return current_user
    return role_checker
