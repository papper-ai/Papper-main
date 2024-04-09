from pydantic import BaseModel
from main_service.src.config import settings

AUTH_SERVICE_URL = settings.auth_service_url


class AuthEndpoints(BaseModel):
    registration: str = f"{AUTH_SERVICE_URL}/personal/registration"
    login: str = f"{AUTH_SERVICE_URL}/personal/token"
    refresh: str = f"{AUTH_SERVICE_URL}/personal/refresh"


auth_endpoints = AuthEndpoints()
