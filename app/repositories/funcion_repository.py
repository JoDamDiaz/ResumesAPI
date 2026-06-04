from sqlalchemy.orm import Session
from app.models.funcion_experiencia import FuncionExperiencia
from app.schemas.funcion_experiencia import FuncionExperienciaCreate, FuncionExperienciaUpdate


class FuncionRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, funcion_id: int) -> FuncionExperiencia | None:
        return (
            self.db.query(FuncionExperiencia)
            .filter(FuncionExperiencia.id == funcion_id)
            .first()
        )

    def get_by_experiencia_id(self, experiencia_id: int) -> list[FuncionExperiencia]:
        return (
            self.db.query(FuncionExperiencia)
            .filter(FuncionExperiencia.experiencia_id == experiencia_id)
            .order_by(FuncionExperiencia.orden)
            .all()
        )

    def create(self, data: FuncionExperienciaCreate) -> FuncionExperiencia:
        funcion = FuncionExperiencia(**data.model_dump())
        self.db.add(funcion)
        self.db.commit()
        self.db.refresh(funcion)
        return funcion

    def bulk_create(self, experiencia_id: int, items: list[dict]) -> list[FuncionExperiencia]:
        funciones = [FuncionExperiencia(experiencia_id=experiencia_id, **item) for item in items]
        self.db.add_all(funciones)
        return funciones

    def update(self, funcion: FuncionExperiencia, data: FuncionExperienciaUpdate) -> FuncionExperiencia:
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(funcion, field, value)
        self.db.commit()
        self.db.refresh(funcion)
        return funcion

    def delete(self, funcion: FuncionExperiencia) -> None:
        self.db.delete(funcion)
        self.db.commit()
