from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.customers.schemas import CustomerCreate, CustomerRead
from app.modules.customers.service import CustomerService

router = APIRouter(prefix="/customers", tags=["Клієнти"])

DbSession = Annotated[Session, Depends(get_db)]


def get_service(db: DbSession) -> CustomerService:
    return CustomerService(db)


Service = Annotated[CustomerService, Depends(get_service)]


@router.get("", response_model=list[CustomerRead], summary="Перелік клієнтів")
def list_customers(service: Service) -> list[CustomerRead]:
    return service.list_customers()


@router.post(
    "",
    response_model=CustomerRead,
    status_code=status.HTTP_201_CREATED,
    summary="Створити клієнта",
)
def create_customer(payload: CustomerCreate, service: Service) -> CustomerRead:
    return service.create_customer(payload)


@router.get("/{customer_id}", response_model=CustomerRead, summary="Отримати клієнта")
def get_customer(customer_id: int, service: Service) -> CustomerRead:
    return service.get_customer(customer_id)
