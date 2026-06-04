from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.schemas.experiencia_user import ExperienciaUserResponse


class UserBase(BaseModel):
    nombre: str
    telefono: Optional[str] = None
    correo: EmailStr
    linkedin: Optional[str] = None
    github: Optional[str] = None
    ubicacion: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    correo: Optional[EmailStr] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    ubicacion: Optional[str] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    experiencias: list[ExperienciaUserResponse] = []


class UserSimpleResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
