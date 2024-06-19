from pathlib import Path
from pydantic import BaseModel, HttpUrl, FilePath
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

BASE_DIR = Path(__file__).parent.parent


class JWTAuth(BaseModel):
    private_key_path: FilePath = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: FilePath = BASE_DIR / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_hours: int = 24


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env", extra="ignore")
    jwt_auth: JWTAuth = JWTAuth()
    redis_host: str
    redis_port: int


settings: Setting = Setting()
