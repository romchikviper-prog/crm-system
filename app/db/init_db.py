import logging

from app.db.base import Base
from app.db.session import engine
from app.modules import customers  # noqa: F401  (реєстрація ORM-моделей)

logger = logging.getLogger(__name__)


def init_db() -> None:
    """Створює таблиці, яких ще немає в базі даних."""
    Base.metadata.create_all(bind=engine)
    logger.info("database schema is ready")
