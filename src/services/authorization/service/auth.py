from src.dependencies import parse_jwt
from ..utils.cache import auth_cache_manager, AuthCache
from ..schemas.credentials import AuthCredentials, RegistrationCredentials
from ..schemas.tokens import JWTTokensResponse, JWTRefreshRequest
from ..utils.requests import request_to_auth_service
from ..external_endpoints import auth_endpoints
from ..utils.create_response import create_response_with_tokens
import aiohttp


class AuthService:
    def __init__(self):
        self.cache_manager: AuthCache = auth_cache_manager

    async def get_login(self, token: str) -> str:
        result = await self.cache_manager.get_login(token)
        if result is None:
            jwt_payload = await parse_jwt(token=token)
            login = jwt_payload.login
            await self.cache_manager.set_login(token=token, login=login)
        else:
            login = result

        return login

    @staticmethod
    async def authorize_user(
        auth_credentials: AuthCredentials,
        client_session: aiohttp.ClientSession,
    ) -> JWTTokensResponse:
        response = await request_to_auth_service(
            endpoint=auth_endpoints.login,
            session=client_session,
            pydantic_model=auth_credentials,
        )
        tokens = await create_response_with_tokens(response=response)
        return tokens

    @staticmethod
    async def register_user(
        registration_credentials: RegistrationCredentials,
        client_session: aiohttp.ClientSession,
    ) -> None:
        await request_to_auth_service(
            endpoint=auth_endpoints.registration,
            session=client_session,
            pydantic_model=registration_credentials,
        )
        return

    @staticmethod
    async def get_new_tokens(
        refresh_token: JWTRefreshRequest,
        client_session: aiohttp.ClientSession,
    ) -> JWTTokensResponse:
        response = await request_to_auth_service(
            endpoint=auth_endpoints.refresh,
            session=client_session,
            pydantic_model=refresh_token,
        )
        tokens = await create_response_with_tokens(response=response)
        return tokens
