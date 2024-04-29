import aiohttp
from fastapi import HTTPException

from src.utils import aiohttp_error_handler
from ..external_endpoints import chats_endpoints
from ...schemas.chat import CreateChat, ChatPayload


@aiohttp_error_handler(service_name="Chat")
async def create_chat_request(
    session: aiohttp.ClientSession,
    pydantic_model: CreateChat,
    endpoint: str = chats_endpoints.create_chat,
) -> ChatPayload:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return ChatPayload(**result)
