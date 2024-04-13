import aiohttp
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi import Depends, Request
from typing import Annotated
from src.auth_service.utils import (
    make_registration_credentials,
    request_to_auth_service,
    create_response_with_tokens,
    make_auth_credentials,
)
from ..schemas import (
    JWTTokensResponse,
    RegistrationCredentials,
    JWTRefreshRequest,
    AuthCredentials,
)
from ..external_endpoints import auth_endpoints
from src.utils import get_aiohttp_session

http_bearer = HTTPBearer()


async def authorize_user(
    auth_credentials: Annotated[
        AuthCredentials,
        Depends(make_auth_credentials),
    ],
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
) -> JWTTokensResponse:
    response = await request_to_auth_service(
        endpoint=auth_endpoints.login, session=client_session, schema=auth_credentials
    )
    tokens = await create_response_with_tokens(response=response)
    return tokens


async def register_user(
    registration_credentials: Annotated[
        RegistrationCredentials,
        Depends(make_registration_credentials),
    ],
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
) -> None:
    await request_to_auth_service(
        endpoint=auth_endpoints.registration,
        session=client_session,
        schema=registration_credentials,
    )
    return


async def get_new_tokens(
    refresh_token: JWTRefreshRequest,
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
) -> JWTTokensResponse:
    response = await request_to_auth_service(
        endpoint=auth_endpoints.refresh, session=client_session, schema=refresh_token
    )
    tokens = await create_response_with_tokens(response=response)
    return tokens
