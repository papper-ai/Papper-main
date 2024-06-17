from pydantic import BaseModel, UUID4


class UserCredentials(BaseModel):
    user_id: UUID4
