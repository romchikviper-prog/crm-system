import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.context import get_request_id

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Базова помилка застосунку з передбачуваним HTTP-статусом."""

    status_code = 400
    code = "bad_request"
    message = "Некоректний запит"

    def __init__(self, message: str | None = None) -> None:
        self.message = message or self.message
        super().__init__(self.message)


class NotFoundError(AppError):
    status_code = 404
    code = "not_found"
    message = "Ресурс не знайдено"


class ConflictError(AppError):
    status_code = 409
    code = "conflict"
    message = "Конфлікт даних"


class UnauthorizedError(AppError):
    status_code = 401
    code = "unauthorized"
    message = "Потрібна автентифікація"


def error_payload(code: str, message: str, details: Any = None) -> dict:
    """Формує єдину структуру відповіді про помилку."""
    payload: dict = {
        "error": {
            "code": code,
            "message": message,
            "request_id": get_request_id(),
        }
    }
    if details is not None:
        payload["error"]["details"] = details
    return payload


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def handle_app_error(request: Request, exc: AppError) -> JSONResponse:
        logger.warning("application error: %s (%s)", exc.message, exc.code)
        return JSONResponse(
            status_code=exc.status_code,
            content=error_payload(exc.code, exc.message),
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        details = [
            {
                "field": ".".join(str(part) for part in error["loc"][1:]),
                "message": error["msg"],
            }
            for error in exc.errors()
        ]
        logger.warning("validation error: %s", details)
        return JSONResponse(
            status_code=422,
            content=error_payload("validation_error", "Помилка валідації даних", details),
        )

    @app.exception_handler(Exception)
    async def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
        logger.exception("unhandled error: %s %s", request.method, request.url.path)
        return JSONResponse(
            status_code=500,
            content=error_payload("internal_error", "Внутрішня помилка сервера"),
        )
