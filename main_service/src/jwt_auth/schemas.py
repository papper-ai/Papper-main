from pydantic import BaseModel, EmailStr, Field, UUID4


class Token(BaseModel):
    token: str
    token_type: str = Field(default="bearer")


class AccessToken(Token):
    pass


class RefreshToken(Token):
    pass


class JWTTokensResponse(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken


class Credentials(BaseModel):
    login: EmailStr
    password: str


class AuthCredentials(Credentials):
    pass


class RegistrationCredentials(Credentials):
    secret: UUID4
    name: str
    surname: str


class JWTRefreshRequest(BaseModel):
    refresh_token: str
