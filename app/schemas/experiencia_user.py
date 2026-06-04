from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date
from app.schemas.funcion_experiencia import FuncionExperienciaInCreate, FuncionExperienciaResponse


class ExperienciaUserBase(BaseModel):
    cargo: str
    empresa: str
    tiempo_inicio: date
    tiempo_final: Optional[date] = None


class ExperienciaUserCreate(ExperienciaUserBase):
    user_id: int
    funciones: list[FuncionExperienciaInCreate] = []


class ExperienciaUserUpdate(BaseModel):
    cargo: Optional[str] = None
    empresa: Optional[str] = None
    tiempo_inicio: Optional[date] = None
    tiempo_final: Optional[date] = None


class ExperienciaUserResponse(ExperienciaUserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    funciones: list[FuncionExperienciaResponse] = []
