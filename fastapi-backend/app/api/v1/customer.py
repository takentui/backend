import logging

from app import models
from app.producer.producer import kafka_producer
from app.producer.rabbit_producer import rabbit_publisher
from app.services.customer import (
    save_business_customer,
    save_business_customer_with_event,
)
from fastapi import APIRouter, status
from starlette.responses import Response

router = APIRouter()


@router.post("/event-inside", status_code=status.HTTP_201_CREATED)
async def persist_business_customer_event_inside(payload: models.CustomerRequest) -> Response:
    customer = await save_business_customer(payload)
    await kafka_producer.produce_message(
        {"uid": str(customer.uid), "type": customer.type_, "in_box": True}
    )
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/out-of-box", status_code=status.HTTP_201_CREATED)
async def persist_business_customer_out_of_box(payload: models.CustomerRequest) -> Response:
    await save_business_customer_with_event(payload)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/message-inside", status_code=status.HTTP_201_CREATED)
async def persist_business_customer_message_inside(payload: models.CustomerRequest) -> Response:
    customer = await save_business_customer(payload)
    rabbit_publisher.send_message(
        "message_type", {"uid": str(customer.uid), "type": customer.type_, "in_box": True}
    )
    return Response(status_code=status.HTTP_201_CREATED)


#
# @router.post("/out-of-box", status_code=status.HTTP_201_CREATED)
# async def persist_business_customer(payload: models.CustomerRequest) -> Response:
#     await save_business_customer_with_event(payload)
#     return Response(status_code=status.HTTP_201_CREATED)
