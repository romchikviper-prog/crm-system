from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.customers.models import Customer


class CustomerRepository:
    """Доступ до даних клієнтів."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list(self) -> list[Customer]:
        statement = select(Customer).order_by(Customer.id)
        return list(self.db.scalars(statement))

    def get(self, customer_id: int) -> Customer | None:
        return self.db.get(Customer, customer_id)

    def get_by_email(self, email: str) -> Customer | None:
        statement = select(Customer).where(Customer.email == email)
        return self.db.scalar(statement)

    def create(self, **data) -> Customer:
        customer = Customer(**data)
        self.db.add(customer)
        self.db.commit()
        self.db.refresh(customer)
        return customer
