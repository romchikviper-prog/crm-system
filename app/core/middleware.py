import logging
import time
import uuid

from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.core.context import request_id_var
from app.core.errors import error_payload

logger = logging.getLogger("app.request")


class RequestContextMiddleware(BaseHTTPMiddleware):
    """Присвоює запиту ідентифікатор, журналює його та перехоплює помилки."""

    async def dispatch(self, request: Request, call_next) -> Response:
        request_id = request.headers.get("X-Request-ID") or uuid.uuid4().hex
        token = request_id_var.set(request_id)
        started = time.perf_counter()
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        try:
            try:
                response = await call_next(request)
                status_code = response.status_code
            except Exception:
                logger.exception("unhandled error: %s %s", request.method, request.url.path)
                response = JSONResponse(
                    status_code=status_code,
                    content=error_payload("internal_error", "Внутрішня помилка сервера"),
                )
            response.headers["X-Request-ID"] = request_id
            return response
        finally:
            elapsed_ms = (time.perf_counter() - started) * 1000
            logger.info(
                "%s %s -> %s (%.1f ms) request_id=%s",
                request.method,
                request.url.path,
                status_code,
                elapsed_ms,
                request_id,
            )
            request_id_var.reset(token)
