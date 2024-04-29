from pydantic import HttpUrl, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

MESSAGING_SERVICE_DIR = Path(__file__).parent


class ChatsServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=MESSAGING_SERVICE_DIR / ".env", extra="ignore"
    )
    chats_service_host: str
    chats_service_port: int

    @property
    def chats_service_url(self) -> HttpUrl:
        return f"http://{self.chats_service_host}:{self.chats_service_port}"


class HistoryServiceSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=MESSAGING_SERVICE_DIR / ".env", extra="ignore"
    )
    history_service_host: str
    history_service_port: int

    @property
    def history_service_url(self) -> HttpUrl:
        return f"http://{self.history_service_host}:{self.history_service_port}"


class Setting(BaseModel):
    chats_service_settings: ChatsServiceSettings = ChatsServiceSettings()
    history_service_settings: HistoryServiceSettings = HistoryServiceSettings()


settings = Setting()
