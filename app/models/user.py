from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(20), nullable=True)
    correo = Column(String(255), unique=True, nullable=False)
    linkedin = Column(String(255), nullable=True)
    github = Column(String(255), nullable=True)
    ubicacion = Column(String(255), nullable=True)

    experiencias = relationship(
        "ExperienciaUser",
        back_populates="user",
        cascade="all, delete-orphan",
        order_by="ExperienciaUser.tiempo_inicio.desc()",
    )
