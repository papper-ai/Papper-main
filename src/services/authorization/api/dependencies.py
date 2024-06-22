from ..service.auth import AuthService


async def get_auth_service() -> AuthService:
    return AuthService()
