import pika
from pydantic import BaseSettings


class RabbitSettings(BaseSettings):
    host: str = "rabbitmq"
    port: int = 5672
    credentials = pika.PlainCredentials("guest", "guest")
    queue_name: str = "test-queue"
    exchange_name: str = "example_exchange"
    exchange_type: str = "fanout"

    class Config:
        env_prefix = "rabbit_"
