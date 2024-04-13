from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

VAULT_SERVICE_DIR = Path(__file__).parent


class Setting(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=VAULT_SERVICE_DIR / ".env", extra="ignore"
    )

    vault_service_host: str
    vault_service_port: int

    @property
    def auth_service_url(self) -> HttpUrl:
        return f"http://{self.vault_service_host}:{self.vault_service_port}"


settings = Setting()
