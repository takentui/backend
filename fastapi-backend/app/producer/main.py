import asyncio

from prometheus_client import start_http_server

from .service import ProducerService


def main() -> None:
    producer_service = ProducerService()
    asyncio.run(producer_service.run())


if __name__ == "__main__":
    start_http_server(8000)
    main()
