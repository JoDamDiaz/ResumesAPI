from fastapi import APIRouter, Depends, status
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

router = APIRouter(prefix="/experiencias", tags=["Experiencia Laboral"])


@router.get("/", response_model=list[ExperienciaUserResponse])
def list_experiencias(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ExperienciaService(db).get_all(skip, limit)


@router.get("/user/{user_id}", response_model=list[ExperienciaUserResponse])
def list_experiencias_by_user(user_id: int, db: Session = Depends(get_db)):
    return ExperienciaService(db).get_by_user_id(user_id)


@router.get("/{experiencia_id}", response_model=ExperienciaUserResponse)
def get_experiencia(experiencia_id: int, db: Session = Depends(get_db)):
    return ExperienciaService(db).get_by_id(experiencia_id)


@router.post("/", response_model=ExperienciaUserResponse, status_code=status.HTTP_201_CREATED)
def create_experiencia(data: ExperienciaUserCreate, db: Session = Depends(get_db)):
    return ExperienciaService(db).create(data)


@router.put("/{experiencia_id}", response_model=ExperienciaUserResponse)
def update_experiencia(
    experiencia_id: int, data: ExperienciaUserUpdate, db: Session = Depends(get_db)
):
    return ExperienciaService(db).update(experiencia_id, data)


@router.delete("/{experiencia_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_experiencia(experiencia_id: int, db: Session = Depends(get_db)):
    ExperienciaService(db).delete(experiencia_id)


# ── Funciones anidadas bajo /experiencias/{id}/funciones ──────────────────────

@router.get("/{experiencia_id}/funciones", response_model=list[FuncionExperienciaResponse])
def list_funciones(experiencia_id: int, db: Session = Depends(get_db)):
    return FuncionService(db).get_by_experiencia(experiencia_id)


@router.post(
    "/{experiencia_id}/funciones",
    response_model=FuncionExperienciaResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_funcion(experiencia_id: int, data: FuncionExperienciaCreate, db: Session = Depends(get_db)):
    data.experiencia_id = experiencia_id
    return FuncionService(db).create(data)
