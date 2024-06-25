from functools import cached_property
from typing import Any

from app import TopicName
from app.config import parse_fallback
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.types import PUBLIC_KEY_TYPES
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from pydantic import BaseSettings, FilePath, validator


class ConsumerSettings(BaseSettings):
    bootstrap_servers: list[str] = ["kafka:9092"]
    connection_timeout: int = 10
    topic: TopicName
    group: str = "kyc_survey_management"
    retry_count: int = 1
    retry_timeout: int = 0
    public_key_path: FilePath | None = None
    jwt_algorithm: str = "RS256"

    @cached_property
    def public_key(self) -> PUBLIC_KEY_TYPES:
        if self.public_key_path is not None:
            return load_pem_public_key(self.public_key_path.read_bytes(), backend=default_backend())
        raise ValueError("You should set public key path!")

    @validator("bootstrap_servers", pre=True)
    @classmethod
    def list_validator(cls, value: Any) -> list[str]:
        value = value or []
        return value if isinstance(value, list) else [value]

    class Config:
        env_prefix = "consumer_"
        json_loads = parse_fallback
        keep_untouched = (cached_property,)
