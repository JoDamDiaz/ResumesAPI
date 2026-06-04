from fastapi import FastAPI
from app.database import Base, engine
from app.models import user, experiencia_user, funcion_experiencia  # noqa: F401
from app.controllers.user_controller import router as user_router
from app.controllers.experiencia_controller import router as experiencia_router
from app.controllers.funcion_controller import router as funcion_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Resumes API",
    description="API REST para gestión de usuarios y experiencia laboral",
    version="2.0.0",
)

app.include_router(user_router, prefix="/api/v1")
app.include_router(experiencia_router, prefix="/api/v1")
app.include_router(funcion_router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "Resumes API en funcionamiento"}
