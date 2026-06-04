from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship
from app.database import Base


class FuncionExperiencia(Base):
    __tablename__ = "funcion_experiencia"

    id = Column(Integer, primary_key=True, autoincrement=True)
    experiencia_id = Column(
        Integer, ForeignKey("experiencia_user.id", ondelete="CASCADE"), nullable=False
    )
    descripcion = Column(Text, nullable=False)
    orden = Column(Integer, default=1, nullable=False)

    experiencia = relationship("ExperienciaUser", back_populates="funciones")
