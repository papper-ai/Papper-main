import aiohttp
from ..schemas.user import UserCredentials
from ..schemas.chat import ChatPayload
from ..requests.external_endpoints import chats_endpoints
from ..requests.chats_service import get_user_chats_request


async def get_user_chats(
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
