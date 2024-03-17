from fastapi.security import (
    HTTPBasic,
    HTTPBasicCredentials,
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from fastapi import Depends, Request
from typing import Annotated
from .utils import make_credentials, request_to_auth_service
from main_service.src.jwt_auth.schemas import (
    JWTTokensResponse,
    RegistrationCredentials,
    JWTRefreshRequest,
)
from .auth_endpoints import auth_endpoints

security = HTTPBasic()
http_bearer = HTTPBearer()


async def authorize_user(
    basic_auth_credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    request: Request,
) -> JWTTokensResponse:
    client_session = request.state.client_session

    response = await request_to_auth_service(
        endpoint=auth_endpoints.login,
        client_session=client_session,
        schema=basic_auth_credentials,
    )
    tokens = JWTTokensResponse(**response)
    return tokens


async def register_user(
    registration_credentials: Annotated[
        RegistrationCredentials,
        Depends(make_credentials),
    ],
    request: Request,
) -> None:
    client_session = request.state.client_session

    await request_to_auth_service(
        endpoint=auth_endpoints.registration,
        client_session=client_session,
        schema=registration_credentials,
    )
    return


async def get_new_tokens(
    token_auth_credentials: Annotated[
        HTTPAuthorizationCredentials, Depends(http_bearer)
    ],
    request: Request,
) -> JWTTokensResponse:
    client_session = request.state.client_session
    token = JWTRefreshRequest(refresh_token=token_auth_credentials.credentials)

    response = await request_to_auth_service(
        endpoint=auth_endpoints.refresh, client_session=client_session, schema=token
    )
    tokens = JWTTokensResponse(**response)
    return tokens
