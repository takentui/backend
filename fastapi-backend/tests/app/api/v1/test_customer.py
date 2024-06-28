from app import app
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
from starlette import status
from tests.factories.models import CustomerRequestFactory


async def test_create_customer_produce_happy_path(client: AsyncClient, mocker):
    payload = CustomerRequestFactory.build()

    mocker.patch("app.producer.producer.SimpleProducer.produce_message")

    response = await client.post(
        app.url_path_for(
            "persist_business_customer_event_inside",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text


async def test_create_customer_produce_event(client: AsyncClient, mocker):
    payload = CustomerRequestFactory.build()

    mocked_sending = mocker.patch("app.producer.producer.SimpleProducer.produce_message")

    response = await client.post(
        app.url_path_for(
            "persist_business_customer_event_inside",
        ),
        json=jsonable_encoder(payload),
    )

    assert response.status_code == status.HTTP_201_CREATED, response.text
    assert mocked_sending.call_count == 1
    assert mocked_sending.call_args[0][0].get("type") == payload.type_
    assert mocked_sending.call_args[0][0].get("in_box") is True
