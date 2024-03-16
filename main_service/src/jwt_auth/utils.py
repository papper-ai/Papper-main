from typing import Annotated
import aiohttp
from fastapi import Form, HTTPException
from fastapi.security import HTTPBasicCredentials
from pydantic import EmailStr, UUID4

from .schemas import RegistrationCredentials, JWTRefreshRequest


async def make_credentials(
    secret: Annotated[UUID4, Form()],
    name: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    login: Annotated[EmailStr, Form()],
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


async def request_to_auth_service(
    endpoint: str,
    client_session: aiohttp.ClientSession,
    schema: RegistrationCredentials | JWTRefreshRequest | HTTPBasicCredentials,
) -> dict:
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    async with client_session.post(
        url=endpoint, data=schema.model_dump_json(), headers=headers
    ) as response:
        result = await response.json()
        if response.status != 200:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return result
