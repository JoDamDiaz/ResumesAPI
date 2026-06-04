from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserSimpleResponse
from app.models.user import User
from app.auth.dependencies import get_current_user
from app.auth.roles import ADMIN, AUDITOR, USUARIO, require_role

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/", response_model=list[UserSimpleResponse])
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == USUARIO:
        # El rol usuario solo ve su propio perfil
        return [UserService(db).get_by_id(current_user.user_id)]
    return UserService(db).get_all(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == USUARIO and current_user.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes ver tu propio perfil")
    return UserService(db).get_by_id(user_id)


@router.post("/", response_model=UserSimpleResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if current_user.role.nombre == AUDITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditores no pueden crear usuarios")
    return UserService(db).create(data)


@router.put("/{user_id}", response_model=UserSimpleResponse)
def update_user(
    user_id: int,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    role = current_user.role.nombre
    if role == AUDITOR:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Auditores no pueden modificar usuarios")
    if role == USUARIO and current_user.user_id != user_id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Solo puedes modificar tu propio perfil")
    return UserService(db).update(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(ADMIN)),
):
    UserService(db).delete(user_id)
