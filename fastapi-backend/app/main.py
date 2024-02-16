import logging.config

from app import api, config
from app.db.registry import registry
from app.producer.producer import kafka_producer
from app.producer.rabbit_producer import rabbit_publisher
from fastapi import FastAPI
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.exceptions import HTTPException

logging.config.dictConfig(config.LOGGING)

app = FastAPI(
    title=config.application.name,
    version=config.application.version,
    debug=config.application.debug,
    docs_url=config.application.docs_url,
    root_path=config.application.root_path,
)

instrumentator = Instrumentator().instrument(app)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)


@app.on_event("startup")
async def _on_startup():
    await registry.setup()
    await kafka_producer.init()
    rabbit_publisher.initialize()
    instrumentator.expose(app)


@app.on_event("shutdown")
async def _on_shutdown():
    await registry.close()
    await kafka_producer.stop()
    rabbit_publisher.close()


app.include_router(api.v1.router, prefix="/api/v1")
