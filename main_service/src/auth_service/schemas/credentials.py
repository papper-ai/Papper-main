from pydantic import BaseModel, UUID4


class Credentials(BaseModel):
    login: str
    password: str


class AuthCredentials(Credentials):
    pass


class RegistrationCredentials(Credentials):
    secret: UUID4
    name: str
    surname: str
