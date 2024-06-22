from fastapi import APIRouter, Depends, status
from typing import Annotated
from ..schemas.tokens import JWTTokensResponse, JWTRefreshRequest
from ..schemas.login import LoginResponse
from .dependencies import get_auth_service
from ..service.auth import AuthService
from ..schemas.credentials import AuthCredentials, RegistrationCredentials
from ..utils.make_credentials import (
    make_auth_credentials,
    make_registration_credentials,
)
import aiohttp
from src.utils import get_aiohttp_session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(prefix="/auth", tags=["Authorization"])

http_bearer = HTTPBearer()


@router.post(
    "/login",
    response_model=JWTTokensResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    auth_credentials: Annotated[
        AuthCredentials,
        Depends(make_auth_credentials),
    ],
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    """
    На вход подаются данные в виде **HTML формы**.
    При успешной регистрации возвращаются 2 токена: access и refresh.\n
    Длина логина 3-20 символов, длина пароля 8-20 символов\n
    """
    jwt_tokens = await auth_service.authorize_user(auth_credentials, client_session)
    return jwt_tokens


@router.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
)
async def registration(
    registration_credentials: Annotated[
        RegistrationCredentials,
        Depends(make_registration_credentials),
    ],
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    """
    На вход подаются данные в виде **HTML формы**.
    При успешной регистрации возвращается статус 201
    Длина логина, имени и фамилии 3-20 символов, длина пароля 8-20 символов.\n
    Также пароль должен соответствовать след. требованиям:
    - должен содержать хотя бы 1 строчную букву
    - должен содержать хотя бы 1 заглавную букву
    - должен содержать хотя бы 1 цифру
    - должен содержать хотя бы 1 спец. символ: `!@#$%^&*()`
    """
    await auth_service.register_user(registration_credentials, client_session)
    return {"message": "Successfully registered"}


@router.post(
    "/token/refresh/access",
    response_model=JWTTokensResponse,
    description="На вход приходит refresh токен в теле запроса.\nПри успешном обновлении возвращаются 2 токена: access и refresh.",
)
async def refresh_tokens(
    refresh_token: JWTRefreshRequest,
    client_session: Annotated[
        aiohttp.ClientSession,
        Depends(get_aiohttp_session),
    ],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    jwt_tokens = await auth_service.get_new_tokens(refresh_token, client_session)
    return jwt_tokens


@router.get(
    "/user-login",
    response_model=LoginResponse,
)
async def get_login(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
    auth_service: Annotated[
        AuthService,
        Depends(get_auth_service),
    ],
):
    token = credentials.credentials
    user_login = await auth_service.get_login(token=token)
    return LoginResponse(login=user_login)
