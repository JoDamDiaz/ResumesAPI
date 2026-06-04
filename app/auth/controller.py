from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.auth.schemas import LoginRequest, RegisterRequest, TokenResponse
from app.auth.utils import hash_password, verify_password, create_token
from app.auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    if repo.get_by_email(data.correo):
        raise HTTPException(status.HTTP_409_CONFLICT, "El correo ya está registrado")

    user = User(
        nombre=data.nombre,
        correo=data.correo,
        hashed_password=hash_password(data.password),
        telefono=data.telefono,
        ubicacion=data.ubicacion,
        linkedin=data.linkedin,
        github=data.github,
        role_id=3,  # usuario por defecto al registrarse
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_token(user.user_id),
        user_id=user.user_id,
        nombre=user.nombre,
        correo=user.correo,
        role=user.role.nombre,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = UserRepository(db).get_by_email(data.correo)
    if not user or not user.hashed_password:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales incorrectas")
    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales incorrectas")
    if not user.is_active:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Cuenta desactivada")

    return TokenResponse(
        access_token=create_token(user.user_id),
        user_id=user.user_id,
        nombre=user.nombre,
        correo=user.correo,
        role=user.role.nombre,
    )


@router.get("/me", response_model=TokenResponse)
def me(current_user: User = Depends(get_current_user)):
    return TokenResponse(
        access_token="",
        user_id=current_user.user_id,
        nombre=current_user.nombre,
        correo=current_user.correo,
        role=current_user.role.nombre,
    )
