import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db

router = APIRouter(tags=["Службові"])
logger = logging.getLogger(__name__)


@router.get("/health", summary="Перевірка стану сервісу")
def health_check(db: Annotated[Session, Depends(get_db)]) -> dict:
    """Перевіряє доступність API та з’єднання з базою даних."""
    database_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        logger.exception("database health check failed")
        database_status = "error"

    return {
        "status": "ok" if database_status == "ok" else "degraded",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "database": database_status,
    }
