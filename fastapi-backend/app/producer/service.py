import asyncio
import logging
import random

from aiokafka import AIOKafkaProducer
from app import config
from app.db import customer_info as db
from app.db.registry import registry
from app.producer.utils import producer_value_serializer
from prometheus_client import Counter
from sqlalchemy import select


class ProducerService:
    async def initialize(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=config.kafka.bootstrap_servers,
        )
        await registry.setup()
        await self._producer.start()
        self._counter = Counter("events", "Count of events", ["status"])

    async def close(self):
        await registry.close()
        await self._producer.stop()

    async def run(self):
        await self.initialize()
        try:
            while True:
                logging.warning("Trying to find event and produce it...")
                async with registry.session() as session:
                    event = (
                        (
                            await session.execute(
                                select(db.Event).where(db.Event.status == 0).limit(1)
                            )
                        )
                        .scalars()
                        .first()
                    )

                    if event:
                        await self._producer.send_and_wait(
                            config.kafka.topic, producer_value_serializer(event.body)
                        )
                        logging.warning("Event %s produced", event.id_)
                        event.status = 1
                        session.add(event)
                        await session.commit()
                    if random.randint(1, 10) > 5:
                        self._counter.labels("success").inc()
                    else:
                        self._counter.labels("failed").inc()

                await asyncio.sleep(5)
        except Exception as exc:
            logging.exception("Something went wrong", exc_info=exc)
        finally:
            await self.close()
