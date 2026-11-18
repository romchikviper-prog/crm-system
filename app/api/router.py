from fastapi import APIRouter

from app.api.v1 import health
from app.modules.customers.router import router as customers_router

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(customers_router)
