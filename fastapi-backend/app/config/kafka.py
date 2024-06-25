from pydantic import BaseSettings


class KafkaSettings(BaseSettings):
    bootstrap_servers: list[str] = ["kafka:9092"]
    topic: str = "test-topic"

    class Config:
        env_prefix = "kafka_"
