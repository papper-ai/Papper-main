from datetime import datetime
from typing import Annotated
from enum import Enum
from .history import HistoryPayload
from pydantic import BaseModel, UUID4, Field


class ArchiveStatusEnum(str, Enum):
    archived = "archive"
    not_archived = "unarchive"


class CreateChat(BaseModel):
    user_id: UUID4
    vault_id: UUID4
    name: str


class ChatCredentials(BaseModel):
    chat_id: UUID4


class ChatPayload(BaseModel):
    id: UUID4
    name: str
    vault_id: UUID4
    is_archived: bool
    created_at: datetime
    chat_history: HistoryPayload | None = None


class UpdateChat(ChatCredentials):
    new_name: Annotated[str, Field(alias="name", max_length=100)] = (
        "Беседа по железобетону"
    )


class ChangeChatArchiveStatus(ChatCredentials):
    archive_action: ArchiveStatusEnum
