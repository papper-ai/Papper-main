import aiohttp
from ..schemas.chat import ChatCredentials
from ..requests.history_service import clean_history_request


async def clean_chat_history(
    chat_credentials: ChatCredentials, session: aiohttp.ClientSession
) -> None:
    await clean_history_request(
        session=session,
        pydantic_model=chat_credentials,
    )
    return
