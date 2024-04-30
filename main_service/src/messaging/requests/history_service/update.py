import aiohttp
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ...schemas.chat import ChatCredentials
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
