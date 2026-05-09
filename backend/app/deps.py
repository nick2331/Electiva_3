from fastapi import Header, HTTPException, status
from app.config import settings


async def require_admin(x_admin_key: str = Header(default="")) -> None:
    if x_admin_key != settings.admin_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso no autorizado. Header X-Admin-Key inválido o ausente.",
        )
