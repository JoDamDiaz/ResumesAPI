from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.funcion_service import FuncionService
from app.schemas.funcion_experiencia import (
    FuncionExperienciaCreate,
    FuncionExperienciaUpdate,
    FuncionExperienciaResponse,
)

router = APIRouter(prefix="/funciones", tags=["Funciones de Experiencia"])


@router.get("/{funcion_id}", response_model=FuncionExperienciaResponse)
def get_funcion(funcion_id: int, db: Session = Depends(get_db)):
    return FuncionService(db).get_by_id(funcion_id)


@router.post("/", response_model=FuncionExperienciaResponse, status_code=status.HTTP_201_CREATED)
def create_funcion(data: FuncionExperienciaCreate, db: Session = Depends(get_db)):
    return FuncionService(db).create(data)


@router.put("/{funcion_id}", response_model=FuncionExperienciaResponse)
def update_funcion(funcion_id: int, data: FuncionExperienciaUpdate, db: Session = Depends(get_db)):
    return FuncionService(db).update(funcion_id, data)


@router.delete("/{funcion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_funcion(funcion_id: int, db: Session = Depends(get_db)):
    FuncionService(db).delete(funcion_id)
