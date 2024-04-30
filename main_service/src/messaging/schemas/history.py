from typing import Annotated

from pydantic import BaseModel, UUID4, Field


class TracebackUnit(BaseModel):
    document_id: UUID4
    information: str


class AIMessage(BaseModel):
    content: str
    traceback: list[TracebackUnit | None]


class UserMessage(BaseModel):
    content: str


class HistoryPayload(BaseModel):
    chat_id: UUID4
    history: list[UserMessage | AIMessage]
