from fastapi import Form, HTTPException, status
from pydantic import UUID4
from typing_extensions import Annotated
from ..schemas import (
    RegistrationCredentials,
    AuthCredentials,
)
from pydantic import ValidationError


async def make_auth_credentials(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> AuthCredentials:
    try:
        credentials = AuthCredentials(
            login=login,
            password=password,
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(validation_error),
        )
    return credentials


async def make_registration_credentials(
    secret: Annotated[UUID4, Form()],
    name: Annotated[str, Form()],
    surname: Annotated[str, Form()],
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
) -> RegistrationCredentials:
    try:
        credentials = RegistrationCredentials(
            secret=secret,
            name=name,
            surname=surname,
            login=login,
            password=password,
        )
    except ValidationError as validation_error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(validation_error),
        )
    return credentials
