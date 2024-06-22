from ..schemas.chat import ChatPayload, ChatCredentials
from ..requests.chats_service import (
    get_chat_request,
    get_user_chats_request,
    get_vault_chats_request,
)
from ..requests.history_service import get_history_request
import aiohttp
import asyncio
from src.vaults.schemas.vault import VaultCredentials
from ..schemas.user import UserCredentials
from ..requests.external_endpoints import chats_endpoints


async def get_chat_by_user_id(
    session: aiohttp.ClientSession,
    chat_credentials: ChatCredentials,
) -> ChatPayload:
    get_chat_request_task = get_chat_request(
        session=session,
        pydantic_model=chat_credentials,
    )
    get_history_request_task = get_history_request(
        session=session, pydantic_model=chat_credentials
    )

    chat_payload, history_payload = await asyncio.gather(
        get_chat_request_task, get_history_request_task
    )

    chat_payload.chat_history = history_payload
    return chat_payload


async def get_chats_by_user_id(
    session: aiohttp.ClientSession,
    user_credentials: UserCredentials,
    is_archived: bool,
) -> list[ChatPayload]:
    endpoint = (
        chats_endpoints.get_user_chats
        if not is_archived
        else chats_endpoints.get_user_archived_chats
    )

    chat_payloads = await get_user_chats_request(
        session=session,
        pydantic_model=user_credentials,
        endpoint=endpoint,
    )
    return chat_payloads


async def get_chats_by_vault_id(
    session: aiohttp.ClientSession,
    vault_credentials: VaultCredentials,
) -> list[ChatPayload]:

    chat_payloads = await get_vault_chats_request(
        session=session,
        pydantic_model=vault_credentials,
    )
    return chat_payloads
