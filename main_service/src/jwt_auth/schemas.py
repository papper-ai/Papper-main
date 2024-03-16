from pydantic import BaseModel, EmailStr, Field, UUID4


class JWTTokensResponse(BaseModel):
    access_token: str
    refresh_token: str


class Credentials(BaseModel):
    login: EmailStr
    password: str


class RegistrationCredentials(Credentials):
    secret: UUID4
    name: str
    surname: str


class JWTRefreshRequest(BaseModel):
    refresh_token: str
