from datetime import datetime, timezone, timedelta
import jwt
from passlib.context import CryptContext
from app.config import settings

_pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(plain: str) -> str:
    return _pwd.hash(plain)


def verify_password(plain: str, hashed: str) -> bool:
    return _pwd.verify(plain, hashed)


def create_token(user_id: int, role: str) -> str:
    exp = datetime.now(timezone.utc) + timedelta(hours=settings.JWT_EXPIRE_HOURS)
    return jwt.encode(
        {"sub": str(user_id), "role": role, "exp": exp},
        settings.JWT_SECRET,
        algorithm="HS256",
    )


def decode_token(token: str) -> dict:
    payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
    return {"user_id": int(payload["sub"]), "role": payload.get("role", "usuario")}
