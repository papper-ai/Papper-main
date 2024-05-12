from pydantic import BaseModel, UUID4, Field
from src.messaging.schemas.history import UserMessageResponse, AIMessageResponse
from src.messaging.schemas.history import AIMessage


class GenerationCredentials(BaseModel):
    vault_id: UUID4
    chat_id: UUID4
    query: str


class AnswerGenerationCredentials(BaseModel):
    vault_id: UUID4 | None
    query: str
    history: list[UserMessageResponse | AIMessageResponse] | None


class ModelAnswer(BaseModel):
    ai_message: AIMessage
    history_exception: dict[bool:str]
    vault_exception: dict[bool:str]
    add_user_message_exception: dict[bool:str]
    add_ai_message_exception: dict[bool:str]
