from urllib import parse

from pydantic import PostgresDsn as PgDsn


class PostgresDsn(PgDsn):
    @property
    def raw_dsn(self) -> str:
        return f"{self.scheme}://{self.user}:{self.password}@{self.host}:{self.port}{self.path}"

    @property
    def server_settings(self) -> None | dict[str, str]:
        if not self.query:
            return None
        return dict(parse.parse_qsl(self.query))
