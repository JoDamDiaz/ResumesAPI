from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.models.user import User


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        return self.repo.get_all(skip, limit)

    def get_by_id(self, user_id: int) -> User:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado",
            )
        return user

    def create(self, data: UserCreate) -> User:
        if self.repo.get_by_email(data.correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Ya existe un usuario con el correo {data.correo}",
            )
        return self.repo.create(data)

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.get_by_id(user_id)
        if data.correo and data.correo != user.correo:
            if self.repo.get_by_email(data.correo):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Ya existe un usuario con el correo {data.correo}",
                )
        return self.repo.update(user, data)

    def delete(self, user_id: int) -> None:
        user = self.get_by_id(user_id)
        self.repo.delete(user)
