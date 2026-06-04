from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.funcion_repository import FuncionRepository
from app.repositories.experiencia_repository import ExperienciaRepository
from app.schemas.funcion_experiencia import FuncionExperienciaCreate, FuncionExperienciaUpdate
from app.models.funcion_experiencia import FuncionExperiencia


class FuncionService:
    def __init__(self, db: Session):
        self.repo = FuncionRepository(db)
        self.exp_repo = ExperienciaRepository(db)

    def get_by_id(self, funcion_id: int) -> FuncionExperiencia:
        funcion = self.repo.get_by_id(funcion_id)
        if not funcion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Función con ID {funcion_id} no encontrada",
            )
        return funcion

    def get_by_experiencia(self, experiencia_id: int) -> list[FuncionExperiencia]:
        self._validate_experiencia_exists(experiencia_id)
        return self.repo.get_by_experiencia_id(experiencia_id)

    def create(self, data: FuncionExperienciaCreate) -> FuncionExperiencia:
        self._validate_experiencia_exists(data.experiencia_id)
        return self.repo.create(data)

    def update(self, funcion_id: int, data: FuncionExperienciaUpdate) -> FuncionExperiencia:
        funcion = self.get_by_id(funcion_id)
        return self.repo.update(funcion, data)

    def delete(self, funcion_id: int) -> None:
        funcion = self.get_by_id(funcion_id)
        self.repo.delete(funcion)

    def _validate_experiencia_exists(self, experiencia_id: int) -> None:
        if not self.exp_repo.get_by_id(experiencia_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experiencia con ID {experiencia_id} no encontrada",
            )
