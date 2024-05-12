from pydantic import BaseModel, UUID4
from src.messaging.schemas.history import UserMessageResponse, AIMessageResponse


class GenerationCredentials(BaseModel):
    vault_id: UUID4
    chat_id: UUID4
    query: str


class AnswerGenerationCredentials(BaseModel):
    vault_id: UUID4 | None
    query: str
    history: list[UserMessageResponse | AIMessageResponse] | None
