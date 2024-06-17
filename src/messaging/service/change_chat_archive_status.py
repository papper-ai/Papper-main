from ..schemas.chat import ChangeChatArchiveStatus
import aiohttp
from ..requests.chats_service import change_chat_archive_status_request
from ..requests.external_endpoints import chats_endpoints


async def change_chat_archive_status(
    change_archive_status_credentials: ChangeChatArchiveStatus,
    session: aiohttp.ClientSession,
) -> None:
    endpoint = (
        chats_endpoints.archive_chat
        if change_archive_status_credentials.archive_action == "archive"
        else chats_endpoints.unarchive_chat
    )
    await change_chat_archive_status_request(
        session=session,
        pydantic_model=change_archive_status_credentials,
        endpoint=endpoint,
    )
    return
