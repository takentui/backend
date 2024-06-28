from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import BigInteger, Column, DateTime
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql.sqltypes import Integer, String

from .registry import registry

Base = registry.base


class Customer(Base):  # type: ignore
    __tablename__ = "customer"

    uid = Column(UUID(as_uuid=True), primary_key=True, index=True)
    type_ = Column("type", String(256), nullable=False)
    registration_date = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False, index=True
    )
    salesforce_id = Column(String(256), nullable=True)
    registration_platform = Column(String(256), nullable=False)
    created_by = Column(String(256), nullable=False)


class Event(Base):  # type: ignore
    __tablename__ = "event_bus_events_event"

    NEW = 0

    id_ = Column("id", BigInteger, primary_key=True)
    topic_name = Column(String(254), nullable=False, index=True)
    producer = Column(String(254), nullable=False)
    body = Column(JSONB)
    status = Column(Integer, nullable=False, default=NEW)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)

    @classmethod
    def create(cls, body: dict) -> "Event":
        return cls(
            topic_name="topic_name",
            producer="producer_name",
            body=jsonable_encoder(body),
        )
