from ..schemas.chat import UpdateChat
import aiohttp
from ..requests.chats_service import set_chat_name_request


async def update_chat_name(
    chat_update_credentials: UpdateChat,
    session: aiohttp.ClientSession,
) -> None:
    await set_chat_name_request(
        session=session,
        pydantic_model=chat_update_credentials,
    )
    return
