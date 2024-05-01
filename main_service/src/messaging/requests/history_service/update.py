import aiohttp
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ...schemas.chat import ChatCredentials
from ...schemas.history import AddUserMessage, AddAIMessage
from ..external_endpoints import history_endpoints


@aiohttp_error_handler(service_name="History")
async def clean_history_request(
    session: aiohttp.ClientSession,
    pydantic_model: ChatCredentials,
    endpoint: str = history_endpoints.clear_history,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return


@aiohttp_error_handler(service_name="History")
async def add_user_message_request(
    session: aiohttp.ClientSession,
    pydantic_model: AddUserMessage,
    endpoint: str = history_endpoints.add_user_message,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return


@aiohttp_error_handler(service_name="History")
async def add_ai_message_request(
    session: aiohttp.ClientSession,
    pydantic_model: AddAIMessage,
    endpoint: str = history_endpoints.add_ai_message,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return
