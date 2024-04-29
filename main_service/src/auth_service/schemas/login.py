from pydantic import BaseModel


class LoginResponse(BaseModel):
    login: str
