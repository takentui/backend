from pydantic import BaseSettings


class AppSettings(BaseSettings):
    name: str = "One more backend"
    version: str = "2023.1"
    docs_url: str = "/docs"
    root_path: str = ""
    debug: bool = False

    log_level: str = "DEBUG"
    log_filter_urls: list[str] = ["/api/v1/ping", "/docs", "/openapi.json", "/metrics"]

    class Config:
        env_prefix = "app_"
