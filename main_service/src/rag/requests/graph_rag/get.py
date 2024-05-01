import aiohttp
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ..external_endpoints import graph_rag_endpoints
from ...schemas.qa import AnswerGenerationCredentials
from src.messaging.schemas.history import AIMessage


@aiohttp_error_handler(service_name="Graph RAG")
async def get_answer_request(
    session: aiohttp.ClientSession,
    pydantic_model: AnswerGenerationCredentials,
    endpoint: str = graph_rag_endpoints.get_answer,
) -> AIMessage:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return AIMessage(**result)
