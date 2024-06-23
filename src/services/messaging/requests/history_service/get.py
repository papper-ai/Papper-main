import aiohttp
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ...schemas.chat import ChatCredentials
from ...schemas.history import HistoryPayload, UserMessageResponse, AIMessageResponse
from ..external_endpoints import history_endpoints


@aiohttp_error_handler(service_name="History")
async def get_history_request(
    session: aiohttp.ClientSession,
    pydantic_model: ChatCredentials,
    endpoint: str = history_endpoints.get_history,
) -> HistoryPayload:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    processed_history = []
    for history in result["history"]:
        if history["role"] == "user":
            processed_history.append(UserMessageResponse(**history))
        else:
            processed_history.append(AIMessageResponse(**history))

    history_payload = HistoryPayload(history=processed_history)
    return history_payload
