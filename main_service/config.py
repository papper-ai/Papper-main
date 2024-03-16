from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
import os

load_dotenv(Path(__file__).parent.parent / ".env")

BASE_DIR = Path(__file__).parent
AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST")
AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT")


class JWTAuth(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_hours: int = 24


class Setting(BaseSettings):
    jwt_auth: JWTAuth = JWTAuth()
    auth_service_url: str = f"http://{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}"
    model_config = SettingsConfigDict(env_ignore_empty=True)


settings: Setting = Setting()
