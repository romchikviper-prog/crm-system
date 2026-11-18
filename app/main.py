import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import __version__
from app.api.router import api_router
from app.core.config import settings
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import RequestContextMiddleware
from app.db.init_db import init_db

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "starting %s v%s (%s)",
        settings.app_name,
        settings.app_version,
        settings.environment,
    )
    init_db()
    yield
    logger.info("stopping %s", settings.app_name)


def create_app() -> FastAPI:
    setup_logging()
    application = FastAPI(
        title=settings.app_name,
        version=__version__,
        description="API CRM-системи для роботи з клієнтами та контролю замовлень",
        lifespan=lifespan,
    )
    application.add_middleware(RequestContextMiddleware)
    register_exception_handlers(application)
    application.include_router(api_router, prefix=settings.api_v1_prefix)

    @application.get("/", include_in_schema=False)
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "version": __version__, "docs": "/docs"}

    return application


app = create_app()
