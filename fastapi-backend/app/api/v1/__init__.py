from fastapi import APIRouter

from . import customer, monitoring

router = APIRouter()
router.include_router(monitoring.router, tags=["monitoring"])
router.include_router(customer.router, prefix="/customer", tags=["customer"])
