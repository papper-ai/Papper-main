from pydantic import BaseModel, UUID4


class TracebackUnit(BaseModel):
    document_id: UUID4
    document_name: str
    information: str


class BaseMessage(BaseModel):
    content: str


class UserMessage(BaseMessage):
    pass


class AIMessage(BaseMessage):
    traceback: list[TracebackUnit | None]


class BaseAddMessage(BaseModel):
    chat_id: UUID4


class AddUserMessage(BaseAddMessage):
    message: UserMessage


class AddAIMessage(BaseAddMessage):
    message: AIMessage


class BaseMessageResponse(BaseMessage):
    role: str


class AIMessageResponse(BaseMessageResponse):
    traceback: list[TracebackUnit | None]


class UserMessageResponse(BaseMessageResponse):
    pass


class HistoryPayload(BaseModel):
    chat_id: UUID4
    history: list[UserMessageResponse | AIMessageResponse | None]