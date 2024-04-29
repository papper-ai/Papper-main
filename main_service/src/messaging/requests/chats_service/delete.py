import aiohttp
from fastapi import HTTPException

from src.utils import aiohttp_error_handler
from ..external_endpoints import chats_endpoints
from ...schemas.chat import ChatCredentials


@aiohttp_error_handler(service_name="Chat")
async def delete_chat_request(
    session: aiohttp.ClientSession,
    pydantic_model: ChatCredentials,
    endpoint: str = chats_endpoints.delete_chat,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.delete(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return
