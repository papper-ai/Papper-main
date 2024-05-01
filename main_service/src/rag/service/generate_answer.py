import aiohttp
from ..requests.graph_rag import get_answer_request
from ..schemas.qa import GenerationCredentials, AnswerGenerationCredentials
from src.vaults.requests.vault_service import get_vault_request
from src.vaults.schemas.vault import VaultCredentials
from src.messaging.schemas.chat import ChatCredentials
from src.messaging.schemas.history import (
    AddUserMessage,
    AddAIMessage,
    AIMessage,
    UserMessage,
)
from src.messaging.requests.history_service import (
    get_history_request,
    add_user_message_request,
    add_ai_message_request,
)
import asyncio


async def generate_answer(
    generation_credentials: GenerationCredentials, session: aiohttp.ClientSession
) -> AIMessage:
    await add_user_message_request(
        session=session,
        pydantic_model=AddUserMessage(
            chat_id=generation_credentials.chat_id,
            message=UserMessage(content=generation_credentials.query),
        ),
    )

    vault_credentials = VaultCredentials(vault_id=generation_credentials.vault_id)
    chat_credentials = ChatCredentials(chat_id=generation_credentials.chat_id)

    get_vault_task = get_vault_request(
        session=session, pydantic_model=vault_credentials
    )
    get_history_task = get_history_request(
        session=session, pydantic_model=chat_credentials
    )

    vault_payload, chat_history = await asyncio.gather(
        get_vault_task, get_history_task, return_exceptions=True
    )

    if isinstance(chat_history, Exception):
        chat_history = None

    if isinstance(vault_payload, Exception):
        vault_payload = None

    answer_generation_credentials = AnswerGenerationCredentials(
        vault_id=vault_payload.id if vault_payload is not None else None,
        query=generation_credentials.query,
        history=chat_history.history if chat_history is not None else [],
    )

    answer = None
    if vault_payload is None:
        answer = await get_answer_request(
            session=session, pydantic_model=answer_generation_credentials
        )

    if vault_payload.type == "graph":
        answer = await get_answer_request(
            session=session, pydantic_model=answer_generation_credentials
        )

    if vault_payload.type == "vector":
        raise NotImplementedError

    await add_ai_message_request(
        session=session,
        pydantic_model=AddAIMessage(
            chat_id=generation_credentials.chat_id,
            message=answer,
        ),
    )
    return answer