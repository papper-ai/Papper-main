from ..schemas.chat import ChatPayload, ChatCredentials
from ..requests.chats_service import get_chat_request
from ..requests.history_service import get_history_request
import aiohttp
import asyncio


async def get_chat(
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
