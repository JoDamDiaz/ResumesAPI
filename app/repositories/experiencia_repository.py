from sqlalchemy.orm import Session
from app.models.experiencia_user import ExperienciaUser
from app.schemas.experiencia_user import ExperienciaUserCreate, ExperienciaUserUpdate


class ExperienciaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[ExperienciaUser]:
        return self.db.query(ExperienciaUser).offset(skip).limit(limit).all()

    def get_by_id(self, experiencia_id: int) -> ExperienciaUser | None:
        return self.db.query(ExperienciaUser).filter(ExperienciaUser.id == experiencia_id).first()

    def get_by_user_id(self, user_id: int) -> list[ExperienciaUser]:
        return (
            self.db.query(ExperienciaUser)
            .filter(ExperienciaUser.user_id == user_id)
            .order_by(ExperienciaUser.tiempo_inicio.desc())
            .all()
        )

    def create(self, data: ExperienciaUserCreate) -> ExperienciaUser:
        payload = data.model_dump(exclude={"funciones"})
        experiencia = ExperienciaUser(**payload)
        self.db.add(experiencia)
        self.db.flush()  # obtiene el id sin cerrar la transacción
        return experiencia

    def update(self, experiencia: ExperienciaUser, data: ExperienciaUserUpdate) -> ExperienciaUser:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(experiencia, field, value)
        self.db.commit()
        self.db.refresh(experiencia)
        return experiencia

    def delete(self, experiencia: ExperienciaUser) -> None:
        self.db.delete(experiencia)
        self.db.commit()
