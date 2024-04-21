from pydantic import BaseModel, UUID4, Field
from typing import Annotated


class Credentials(BaseModel):
    login: Annotated[str, Field(min_length=3, max_length=32)]
    password: Annotated[
        str,
        Field(
            min_length=8,
            max_length=20,
            pattern=r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()]).*$",
        ),
    ]


class AuthCredentials(Credentials):
    pass


class RegistrationCredentials(Credentials):
    secret: UUID4
    name: Annotated[str, Field(min_length=3, max_length=32)]
    surname: Annotated[str, Field(min_length=3, max_length=32)]
