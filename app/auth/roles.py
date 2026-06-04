from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.auth.dependencies import get_current_user

ADMIN   = "admin"
AUDITOR = "auditor"
USUARIO = "usuario"


def require_role(*roles: str):
    """Dependency factory: verifica que el usuario autenticado tenga uno de los roles indicados."""
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.nombre not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Acceso denegado")
        return current_user
    return dependency
