from typing import Annotated
import aiohttp
from fastapi import Form, HTTPException, status
from pydantic import EmailStr, UUID4

from .schemas import (
    RegistrationCredentials,
    JWTRefreshRequest,
    AuthCredentials,
    JWTTokensResponse,
    AccessToken,
    RefreshToken,
)


async def make_auth_credentials(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> AuthCredentials:
    credentials = AuthCredentials(
        login=login,
        password=password,
    )
    return credentials


async def make_registration_credentials(
    secret: Annotated[UUID4, Form()],
    name: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> RegistrationCredentials:
    credentials = RegistrationCredentials(
        secret=secret,
        name=name,
        surname=surname,
        login=login,
        password=password,
    )
    return credentials


async def create_response_with_tokens(
    response: dict,
) -> JWTTokensResponse:
    access_token = AccessToken(token=response["access_token"])
    refresh_token = RefreshToken(token=response["refresh_token"])
    tokens = JWTTokensResponse(access_token=access_token, refresh_token=refresh_token)
    return tokens


async def request_to_auth_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    schema: RegistrationCredentials | JWTRefreshRequest | AuthCredentials,
) -> dict:
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    async with session.post(
        url=endpoint, data=schema.model_dump_json(), headers=headers
    ) as response:
        result = await response.json()
        if response.status != 200:
            if response.status == 422:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=result["detail"],
                )
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return result
