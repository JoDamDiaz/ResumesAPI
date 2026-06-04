"""
ASGI entry point — compatible con uvicorn y gunicorn + UvicornWorker.

Desarrollo:
    uvicorn asgi:app --reload --host 0.0.0.0 --port 8000

Producción (gunicorn orquesta workers ASGI):
    gunicorn asgi:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
"""
from app.main import app  # noqa: F401 — re-exportado para que uvicorn/gunicorn lo encuentre
