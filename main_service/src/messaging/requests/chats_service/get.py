import aiohttp
from fastapi import HTTPException

from src.utils import aiohttp_error_handler
from ...schemas.user import UserCredentials
from ...schemas.chat import ChatPayload
from ..external_endpoints import chats_endpoints


@aiohttp_error_handler(service_name="Chat")
async def get_user_chats_request(
    session: aiohttp.ClientSession,
    pydantic_model: UserCredentials,
    endpoint: str,
) -> list[ChatPayload]:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.get(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return [ChatPayload(**chat) for chat in result]
