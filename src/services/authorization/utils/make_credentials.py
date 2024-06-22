from fastapi import Form, HTTPException, status
from pydantic import UUID4
from typing_extensions import Annotated
from ..schemas.credentials import (
    RegistrationCredentials,
    AuthCredentials,
)
from pydantic import ValidationError


async def make_auth_credentials(
    login: Annotated[str, Form(min_length=3, max_length=32)],
    password: Annotated[str, Form(min_length=8, max_length=20)],
) -> AuthCredentials:
    try:
        credentials = AuthCredentials(
            login=login,
            password=password,
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.json(),
        )
    return credentials


async def make_registration_credentials(
    secret: Annotated[UUID4, Form()],
    login: Annotated[str, Form(min_length=3, max_length=32)],
    password: Annotated[str, Form(min_length=8, max_length=20)],
) -> RegistrationCredentials:
    try:
        credentials = RegistrationCredentials(
            secret=secret,
            name="bibka",
            surname="bibkov",
            login=login,
            password=password,
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.json(),
        )
    return credentials
