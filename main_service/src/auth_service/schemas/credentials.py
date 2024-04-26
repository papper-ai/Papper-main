from pydantic import BaseModel, UUID4, Field, field_validator
from typing import Annotated
from fastapi import HTTPException, status
import re


class BaseCredentials(BaseModel):
    password: str

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


class AuthCredentials(BaseCredentials):
    login: str
    password: str


class RegistrationCredentials(BaseCredentials):
    secret: UUID4
    name: str
    surname: str
    login: str
    password: str
