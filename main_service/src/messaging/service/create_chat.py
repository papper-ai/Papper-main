import aiohttp
from ..schemas.chat import CreateChat, ChatCredentials, ChatPayload
from ..requests.chats_service import create_chat_request, delete_chat_request
from ..requests.history_service import create_history_request


async def create_chat(
    registration_credentials: CreateChat, session: aiohttp.ClientSession
) -> ChatPayload:
    try:
        chat_payload = await create_chat_request(
            session=session,
            pydantic_model=registration_credentials,
        )
    except Exception:
        raise

    try:
        await create_history_request(
            session=session,
            pydantic_model=ChatCredentials(chat_id=chat_payload.chat_id),
        )
    except Exception:
        await delete_chat_request(
            session=session,
            pydantic_model=ChatCredentials(chat_id=chat_payload.chat_id),
        )
        raise

    return chat_payload
