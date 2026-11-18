from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="-")


def get_request_id() -> str:
    """Повертає ідентифікатор поточного запиту."""
    return request_id_var.get()
