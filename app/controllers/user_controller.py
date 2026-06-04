from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.user_service import UserService
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserSimpleResponse

router = APIRouter(prefix="/users", tags=["Usuarios"])


@router.get("/", response_model=list[UserSimpleResponse])
def list_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return UserService(db).get_all(skip, limit)


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return UserService(db).get_by_id(user_id)


@router.post("/", response_model=UserSimpleResponse, status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    return UserService(db).create(data)


@router.put("/{user_id}", response_model=UserSimpleResponse)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    return UserService(db).update(user_id, data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    UserService(db).delete(user_id)
