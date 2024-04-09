from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

AUTH_SERVICE_DIR = Path(__file__).parent


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=AUTH_SERVICE_DIR / ".env", extra="ignore"
    )

    auth_service_host: str
    auth_service_port: int

    @property
    def auth_service_url(self) -> HttpUrl:
        return f"http://{self.auth_service_host}:{self.auth_service_port}"


settings = Setting()
