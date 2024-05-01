from typing import Annotated

from pydantic import BaseModel, UUID4, Field


class TracebackUnit(BaseModel):
    document_id: UUID4
    information: str


class BaseMessage(BaseModel):
    content: str


class UserMessage(BaseMessage):
    pass


class AIMessage(BaseMessage):
    traceback: list[TracebackUnit | None]


class AddUserMessage(BaseModel):
    chat_id: UUID4
    message: UserMessage


class AddAIMessage(BaseModel):
    chat_id: UUID4
    message: AIMessage


class AIMessageResponse(BaseModel):
    role: str
    content: str
    traceback: list[TracebackUnit | None]


class UserMessageResponse(BaseModel):
    role: str
    content: str


class HistoryPayload(BaseModel):
    chat_id: UUID4
    history: list[UserMessageResponse | AIMessageResponse]
