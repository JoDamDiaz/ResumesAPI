from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class ExperienciaUser(Base):
    __tablename__ = "experiencia_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    cargo = Column(String(255), nullable=False)
    empresa = Column(String(255), nullable=False)
    tiempo_inicio = Column(Date, nullable=False)
    tiempo_final = Column(Date, nullable=True)  # NULL = empleo actual

    user = relationship("User", back_populates="experiencias")
    funciones = relationship(
        "FuncionExperiencia",
        back_populates="experiencia",
        cascade="all, delete-orphan",
        order_by="FuncionExperiencia.orden",
    )
