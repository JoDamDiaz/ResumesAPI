from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, SessionLocal
from app.models import user, experiencia_user, funcion_experiencia  # noqa: F401
from app.models import role as role_model  # noqa: F401  — debe importarse antes del create_all
from app.controllers.user_controller import router as user_router
from app.controllers.experiencia_controller import router as experiencia_router
from app.controllers.funcion_controller import router as funcion_router
from app.auth.controller import router as auth_router


def _seed_initial_data() -> None:
    from app.repositories.user_repository import UserRepository
    from app.auth.utils import hash_password
    from app.models.user import User
    from app.models.role import Role

    db = SessionLocal()
    try:
        # Crear roles base si no existen
        for rid, nombre in [(1, "admin"), (2, "auditor"), (3, "usuario")]:
            if not db.query(Role).filter(Role.role_id == rid).first():
                db.add(Role(role_id=rid, nombre=nombre))
        db.commit()

        repo = UserRepository(db)

        # Usuario administrador
        if not repo.get_by_email("admin@resumes.com"):
            db.add(User(
                nombre="Administrador",
                correo="admin@resumes.com",
                hashed_password=hash_password("Admin1234!"),
                ubicacion="Ciudad de México, MX",
                role_id=1,
            ))
            db.commit()

        # Usuario demo (rol usuario)
        if not repo.get_by_email("demo@resumes.com"):
            db.add(User(
                nombre="Usuario Demo",
                correo="demo@resumes.com",
                hashed_password=hash_password("Demo1234!"),
                ubicacion="Ciudad de México, MX",
                role_id=3,
            ))
            db.commit()
    finally:
        db.close()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    _seed_initial_data()
    yield


app = FastAPI(
    title="Resumes API",
    description="API REST para gestión de usuarios y experiencia laboral",
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router,        prefix="/api/v1")
app.include_router(user_router,        prefix="/api/v1")
app.include_router(experiencia_router, prefix="/api/v1")
app.include_router(funcion_router,     prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Resumes API en funcionamiento"}
