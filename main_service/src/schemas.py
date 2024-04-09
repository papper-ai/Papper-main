from pydantic import BaseModel


class JWTPayload(BaseModel):
    sub: str
    exp: int
