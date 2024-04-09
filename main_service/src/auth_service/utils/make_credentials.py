from fastapi import Form
from pydantic import UUID4
from typing_extensions import Annotated
from ..schemas import (
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
