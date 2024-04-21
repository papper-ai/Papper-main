from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Annotated
from fastapi import HTTPException, status
import re


class Credentials(BaseModel):
    login: Annotated[str, Field(min_length=3, max_length=32)]
    password: Annotated[str, Field(min_length=8, max_length=20)]

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        pattern = re.compile(r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()]).*$")
        if not pattern.match(value):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one digit, one lowercase letter, one uppercase letter, and one special character.",
            )
        return value


class AuthCredentials(Credentials):
    pass


class RegistrationCredentials(Credentials):
    secret: UUID4
    name: Annotated[str, Field(min_length=3, max_length=32)]
    surname: Annotated[str, Field(min_length=3, max_length=32)]
