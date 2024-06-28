import uuid

from app import models
from app.db import customer_info as db
from app.db.registry import registry


async def save_business_customer(data: models.CustomerRequest) -> db.Customer:
    async with registry.session() as session:
        customer = db.Customer(**data.dict(), uid=uuid.uuid4())
        session.add(customer)
        await session.commit()
    return customer


async def save_business_customer_with_event(data: models.CustomerRequest) -> None:
    async with registry.session() as session:
        customer = db.Customer(**data.dict(), uid=uuid.uuid4())
        session.add(customer)
        await session.flush()

        session.add(
            db.Event.create({"uid": str(customer.uid), "type": customer.type_, "in_box": False})
        )
        await session.commit()
