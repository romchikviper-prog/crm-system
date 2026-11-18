from fastapi import APIRouter

from app.core.config import settings

router = APIRouter(tags=["Службові"])


@router.get("/health", summary="Перевірка стану сервісу")
def health_check() -> dict:
    """Повертає базову інформацію про стан сервісу."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
