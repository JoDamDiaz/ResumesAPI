from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.experiencia_repository import ExperienciaRepository
from app.repositories.funcion_repository import FuncionRepository
from app.repositories.user_repository import UserRepository
from app.schemas.experiencia_user import ExperienciaUserCreate, ExperienciaUserUpdate
from app.models.experiencia_user import ExperienciaUser


class ExperienciaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ExperienciaRepository(db)
        self.funcion_repo = FuncionRepository(db)
        self.user_repo = UserRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ExperienciaUser]:
        return self.repo.get_all(skip, limit)

    def get_by_id(self, experiencia_id: int) -> ExperienciaUser:
        exp = self.repo.get_by_id(experiencia_id)
        if not exp:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Experiencia con ID {experiencia_id} no encontrada",
            )
        return exp

    def get_by_user_id(self, user_id: int) -> list[ExperienciaUser]:
        self._validate_user_exists(user_id)
        return self.repo.get_by_user_id(user_id)

    def create(self, data: ExperienciaUserCreate) -> ExperienciaUser:
        self._validate_user_exists(data.user_id)
        experiencia = self.repo.create(data)
        if data.funciones:
            funciones_data = [f.model_dump() for f in data.funciones]
            self.funcion_repo.bulk_create(experiencia.id, funciones_data)
        self.db.commit()
        self.db.refresh(experiencia)
        return experiencia

    def update(self, experiencia_id: int, data: ExperienciaUserUpdate) -> ExperienciaUser:
        exp = self.get_by_id(experiencia_id)
        return self.repo.update(exp, data)

    def delete(self, experiencia_id: int) -> None:
        exp = self.get_by_id(experiencia_id)
        self.repo.delete(exp)

    def _validate_user_exists(self, user_id: int) -> None:
        if not self.user_repo.get_by_id(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado",
            )
