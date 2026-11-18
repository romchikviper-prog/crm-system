from sqlalchemy.orm import Session

from app.core.errors import ConflictError, NotFoundError
from app.modules.customers.models import Customer
from app.modules.customers.repository import CustomerRepository
from app.modules.customers.schemas import CustomerCreate


class CustomerService:
    """Бізнес-правила роботи з клієнтами."""

    def __init__(self, db: Session) -> None:
        self.repository = CustomerRepository(db)

    def list_customers(self) -> list[Customer]:
        return self.repository.list()

    def get_customer(self, customer_id: int) -> Customer:
        customer = self.repository.get(customer_id)
        if customer is None:
            raise NotFoundError(f"Клієнта з ідентифікатором {customer_id} не знайдено")
        return customer

    def create_customer(self, payload: CustomerCreate) -> Customer:
        if self.repository.get_by_email(payload.email) is not None:
            raise ConflictError(f"Клієнт з електронною поштою {payload.email} вже існує")
        return self.repository.create(**payload.model_dump())
