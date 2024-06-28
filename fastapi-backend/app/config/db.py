from typing import Protocol

from app.config.types import PostgresDsn
from pydantic import BaseSettings


class DBConfig(Protocol):
    pool_size: int
    pool_max_overflow: int
    pool_recycle: int
    pool_timeout: int
    dsn: PostgresDsn


class DBSettings(BaseSettings):
    pool_size: int = 5
    pool_max_overflow: int = 10
    pool_recycle: int = 29
    pool_timeout: int = 10
    dsn: PostgresDsn

    class Config:
        env_prefix = "databases_"
