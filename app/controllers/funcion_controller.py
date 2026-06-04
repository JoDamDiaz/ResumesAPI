from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.funcion_service import FuncionService
from app.services.experiencia_service import ExperienciaService
from app.schemas.funcion_experiencia import (
    FuncionExperienciaCreate,
    FuncionExperienciaUpdate,
    FuncionExperienciaResponse,
)
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.roles import ADMIN, AUDITOR, USUARIO, require_role

router = APIRouter(prefix="/funciones", tags=["Funciones de Experiencia"])


def _assert_funcion_ownership(funcion, current_user: User) -> None:
    if current_user.role.nombre == USUARIO and funcion.experiencia.user_id != current_user.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes acceso a esta función")


@router.get("/{funcion_id}", response_model=FuncionExperienciaResponse)
def get_funcion(
    funcion_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    funcion = FuncionService(db).get_by_id(funcion_id)
    _assert_funcion_ownership(funcion, current_user)
    return funcion


@router.post("/", response_model=FuncionExperienciaResponse, status_code=status.HTTP_201_CREATED)
def create_funcion(
    data: FuncionExperienciaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == AUDITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditores no pueden crear funciones")
    if current_user.role.nombre == USUARIO:
        exp = ExperienciaService(db).get_by_id(data.experiencia_id)
        if exp.user_id != current_user.user_id:
            raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes agregar funciones a tus propias experiencias")
    return FuncionService(db).create(data)


@router.put("/{funcion_id}", response_model=FuncionExperienciaResponse)
def update_funcion(
    funcion_id: int,
    data: FuncionExperienciaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    funcion = FuncionService(db).get_by_id(funcion_id)
    _assert_funcion_ownership(funcion, current_user)
    return FuncionService(db).update(funcion_id, data)


@router.delete("/{funcion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_funcion(
    funcion_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(ADMIN)),
):
    FuncionService(db).delete(funcion_id)
