from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

BASE_DIR = Path(__file__).parent.parent


class JWTAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_hours: int = 24


class Setting(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR.parent / ".env", extra="ignore")

    jwt_auth: JWTAuth = JWTAuth()


settings: Setting = Setting()
