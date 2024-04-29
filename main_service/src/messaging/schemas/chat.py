from datetime import datetime

from pydantic import BaseModel, UUID4


class CreateChat(BaseModel):
    user_id: UUID4
    vault_id: UUID4
    name: str


class ChatCredentials(BaseModel):
    chat_id: UUID4


class ChatPayload(ChatCredentials):
    name: str
    vault_id: UUID4
    is_archived: bool
    created_at: datetime
