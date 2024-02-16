import logging

from aiokafka import AIOKafkaProducer
from app import config

from .utils import producer_value_serializer

log = logging.getLogger("uvicorn")


class SimpleProducer:
    async def init(self):
        self.producer = create_producer()
        await self.producer.start()

    async def stop(self):
        await self.producer.stop()

    async def produce_message(self, message: dict) -> dict:
        return await self.producer.send_and_wait(
            config.kafka.topic, producer_value_serializer(message)
        )


def create_producer() -> AIOKafkaProducer:
    return AIOKafkaProducer(
        bootstrap_servers=config.kafka.bootstrap_servers,
    )


kafka_producer = SimpleProducer()
