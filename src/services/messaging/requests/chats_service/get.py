import aiohttp
from fastapi import HTTPException
from src.vaults.schemas.vault import VaultCredentials
from src.utils import aiohttp_error_handler
from ...schemas.user import UserCredentials
from ...schemas.chat import ChatPayload, ChatCredentials
from ..external_endpoints import chats_endpoints


@aiohttp_error_handler(service_name="Chat")
async def get_user_chats_request(
    session: aiohttp.ClientSession,
    pydantic_model: UserCredentials,
    endpoint: str,
) -> list[ChatPayload]:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return [ChatPayload(**chat) for chat in result]


@aiohttp_error_handler(service_name="Chat")
async def get_chat_request(
    session: aiohttp.ClientSession,
    pydantic_model: ChatCredentials,
    endpoint: str = chats_endpoints.get_chat_by_id,
) -> ChatPayload:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return ChatPayload(**result)


@aiohttp_error_handler(service_name="Chat")
async def get_vault_chats_request(
    session: aiohttp.ClientSession,
    pydantic_model: VaultCredentials,
    endpoint: str = chats_endpoints.get_vault_chats,
) -> list[ChatPayload]:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return [ChatPayload(**chat) for chat in result]
