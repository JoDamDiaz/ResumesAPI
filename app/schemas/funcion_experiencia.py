from pydantic import BaseModel, ConfigDict
from typing import Optional


class FuncionExperienciaInCreate(BaseModel):
    """Usado al crear una experiencia con funciones embebidas."""
    descripcion: str
    orden: int = 1


class FuncionExperienciaCreate(BaseModel):
    experiencia_id: int
    descripcion: str
    orden: int = 1


class FuncionExperienciaUpdate(BaseModel):
    descripcion: Optional[str] = None
    orden: Optional[int] = None


class FuncionExperienciaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    experiencia_id: int
    descripcion: str
    orden: int
