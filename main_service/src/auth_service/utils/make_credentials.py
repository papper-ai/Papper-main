from fastapi import Form, HTTPException, status
from pydantic import UUID4
from typing_extensions import Annotated
from ..schemas import (
    RegistrationCredentials,
    AuthCredentials,
)
from fastapi.responses import JSONResponse
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
    name: Annotated[str, Form(min_length=3, max_length=32)],
    surname: Annotated[str, Form(min_length=3, max_length=32)],
    login: Annotated[str, Form(min_length=3, max_length=32)],
    password: Annotated[str, Form(min_length=8, max_length=20)],
) -> RegistrationCredentials:
    try:
        credentials = RegistrationCredentials(
            secret=secret.hex,
            name=name,
            surname=surname,
            login=login,
            password=password,
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=validation_error.json(),
        )
    return credentials
