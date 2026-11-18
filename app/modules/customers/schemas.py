from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    """Дані для створення клієнта."""

    full_name: str = Field(min_length=2, max_length=120, description="ПІБ клієнта")
    email: EmailStr = Field(description="Електронна пошта")
    phone: str | None = Field(default=None, max_length=32, description="Телефон")
    company: str | None = Field(default=None, max_length=120, description="Компанія")


class CustomerRead(BaseModel):
    """Дані клієнта у відповіді API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: EmailStr
    phone: str | None
    company: str | None
    status: str
    created_at: datetime
