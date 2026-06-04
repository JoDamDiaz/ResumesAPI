from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.experiencia_service import ExperienciaService
from app.services.funcion_service import FuncionService
from app.schemas.experiencia_user import (
    ExperienciaUserCreate,
    ExperienciaUserUpdate,
    ExperienciaUserResponse,
)
from app.schemas.funcion_experiencia import (
    FuncionExperienciaCreate,
    FuncionExperienciaResponse,
)
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.roles import ADMIN, AUDITOR, USUARIO, require_role

router = APIRouter(prefix="/experiencias", tags=["Experiencia Laboral"])


def _assert_exp_ownership(experiencia, current_user: User) -> None:
    if current_user.role.nombre == USUARIO and experiencia.user_id != current_user.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No tienes acceso a esta experiencia")


@router.get("/", response_model=list[ExperienciaUserResponse])
def list_experiencias(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == USUARIO:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Acceso denegado")
    return ExperienciaService(db).get_all(skip, limit)


@router.get("/user/{user_id}", response_model=list[ExperienciaUserResponse])
def list_experiencias_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == USUARIO and current_user.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes ver tus propias experiencias")
    return ExperienciaService(db).get_by_user_id(user_id)


@router.get("/{experiencia_id}", response_model=ExperienciaUserResponse)
def get_experiencia(
    experiencia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = ExperienciaService(db).get_by_id(experiencia_id)
    _assert_exp_ownership(exp, current_user)
    return exp


@router.post("/", response_model=ExperienciaUserResponse, status_code=status.HTTP_201_CREATED)
def create_experiencia(
    data: ExperienciaUserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == AUDITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditores no pueden crear experiencias")
    if current_user.role.nombre == USUARIO and data.user_id != current_user.user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes crear experiencias para ti mismo")
    return ExperienciaService(db).create(data)


@router.put("/{experiencia_id}", response_model=ExperienciaUserResponse)
def update_experiencia(
    experiencia_id: int,
    data: ExperienciaUserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = ExperienciaService(db).get_by_id(experiencia_id)
    _assert_exp_ownership(exp, current_user)
    return ExperienciaService(db).update(experiencia_id, data)


@router.delete("/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiencia(
    experiencia_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(ADMIN)),
):
    ExperienciaService(db).delete(experiencia_id)


# ── Funciones anidadas bajo /experiencias/{id}/funciones ──────────────────────

@router.get("/{experiencia_id}/funciones", response_model=list[FuncionExperienciaResponse])
def list_funciones(
    experiencia_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exp = ExperienciaService(db).get_by_id(experiencia_id)
    _assert_exp_ownership(exp, current_user)
    return FuncionService(db).get_by_experiencia(experiencia_id)


@router.post(
    "/{experiencia_id}/funciones",
    response_model=FuncionExperienciaResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_funcion(
    experiencia_id: int,
    data: FuncionExperienciaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == AUDITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditores no pueden crear funciones")
    exp = ExperienciaService(db).get_by_id(experiencia_id)
    _assert_exp_ownership(exp, current_user)
    data.experiencia_id = experiencia_id
    return FuncionService(db).create(data)
