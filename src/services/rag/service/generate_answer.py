import aiohttp
from ..requests.qa import get_answer_request
from ..schemas.qa import GenerationCredentials, AnswerGenerationCredentials, ModelAnswer
from src.services.vaults.schemas.vault import VaultCredentials
from src.services.messaging.schemas.chat import ChatCredentials
from src.services.messaging.schemas.history import (
    AddUserMessage,
    AddAIMessage,
    AIMessageResponse,
    UserMessage,
)
from src.services.messaging.requests.history_service import (
    get_history_request,
    add_user_message_request,
    add_ai_message_request,
)
from ..utils import truncate_history
from ..requests.external_endpoints import rag_endpoints
import asyncio

from src.services.messaging.service.messaging import MessagingService
from ...vaults.service.vaults import VaultsService


async def generate_answer(
    messaging_service: MessagingService,
    vaults_service: VaultsService,
    generation_credentials: GenerationCredentials,
    session: aiohttp.ClientSession,
) -> ModelAnswer:
    history_error = None
    vault_error = None
    add_user_message_error = None
    add_ai_message_error = None

    vault_credentials = VaultCredentials(vault_id=generation_credentials.vault_id)
    chat_credentials = ChatCredentials(chat_id=generation_credentials.chat_id)

    get_vault = vaults_service.get_vault(
        session=session, vault_credentials=vault_credentials
    )
    get_history = get_history_request(session=session, pydantic_model=chat_credentials)

    vault_payload, chat_history = await asyncio.gather(
        get_vault, get_history, return_exceptions=True
    )

    try:
        await add_user_message_request(
            session=session,
            pydantic_model=AddUserMessage(
                chat_id=generation_credentials.chat_id,
                message=UserMessage(content=generation_credentials.query),
            ),
        )
    except Exception as generic_error:
        add_user_message_error = str(generic_error)

    if isinstance(chat_history, Exception):
        history_error = str(chat_history)
        chat_history = None

    if isinstance(vault_payload, Exception):
        vault_error = str(vault_payload)
        vault_payload = None

    history = (
        await truncate_history(chat_history.history, max_tokens=3000)
        if chat_history is not None
        else []
    )
    answer_generation_credentials = AnswerGenerationCredentials(
        vault_id=vault_payload.id if vault_payload is not None else None,
        query=generation_credentials.query,
        history=history,
    )

    answer = None
    if vault_payload is None:
        answer = await get_answer_request(
            session=session,
            pydantic_model=answer_generation_credentials,
            endpoint=rag_endpoints.graph_answer,
        )
    else:
        if vault_payload.type == "graph":
            answer = await get_answer_request(
                session=session,
                pydantic_model=answer_generation_credentials,
                endpoint=rag_endpoints.graph_answer,
            )

        if vault_payload.type == "vector":
            answer = await get_answer_request(
                session=session,
                pydantic_model=answer_generation_credentials,
                endpoint=rag_endpoints.vector_answer,
            )

    try:
        await add_ai_message_request(
            session=session,
            pydantic_model=AddAIMessage(
                chat_id=generation_credentials.chat_id,
                message=answer,
            ),
        )
    except Exception as generic_error:
        add_ai_message_error = str(generic_error)

    history_exception = (
        {True: history_error} if history_error is not None else {False: ""}
    )
    vault_exception = {True: vault_error} if vault_error is not None else {False: ""}
    add_ai_message_exception = (
        {True: add_ai_message_error}
        if add_ai_message_error is not None
        else {False: ""}
    )
    add_user_message_exception = (
        {True: add_user_message_error}
        if add_user_message_error is not None
        else {False: ""}
    )

    if not history_error:
        await messaging_service.cache_manager.delete_chat(
            chat_id=generation_credentials.chat_id
        )

    return ModelAnswer(
        ai_message=AIMessageResponse(**answer.model_dump(), role="ai"),
        history_exception=history_exception,
        vault_exception=vault_exception,
        add_ai_message_exception=add_ai_message_exception,
        add_user_message_exception=add_user_message_exception,
    )
