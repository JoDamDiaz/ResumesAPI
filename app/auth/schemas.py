from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    correo: EmailStr
    password: str


class RegisterRequest(BaseModel):
    nombre: str
    correo: EmailStr
    password: str
    telefono: str | None = None
    ubicacion: str | None = None
    linkedin: str | None = None
    github: str | None = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    nombre: str
    correo: str
