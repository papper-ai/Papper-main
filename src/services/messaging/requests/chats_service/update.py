import aiohttp
from fastapi import HTTPException

from src.utils import aiohttp_error_handler
from ...schemas.chat import ChatCredentials, UpdateChat
from ..external_endpoints import chats_endpoints


@aiohttp_error_handler(service_name="Chat")
async def set_chat_name_request(
    session: aiohttp.ClientSession,
    pydantic_model: UpdateChat,
    endpoint: str = chats_endpoints.set_chat_name,
) -> None:
    json_data = pydantic_model.model_dump(mode="json", by_alias=True)

    async with session.patch(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return


@aiohttp_error_handler(service_name="Chat")
async def change_chat_archive_status_request(
    session: aiohttp.ClientSession,
    pydantic_model: ChatCredentials,
    endpoint: str,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.patch(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return
