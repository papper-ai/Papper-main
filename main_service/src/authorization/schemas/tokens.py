from pydantic import BaseModel, Field


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


class JWTRefreshRequest(BaseModel):
    refresh_token: str
