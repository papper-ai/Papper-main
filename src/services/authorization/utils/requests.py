import aiohttp
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ..schemas.credentials import RegistrationCredentials, AuthCredentials
from ..schemas.tokens import JWTRefreshRequest


@aiohttp_error_handler(service_name="Authorization")
async def request_to_auth_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: RegistrationCredentials | JWTRefreshRequest | AuthCredentials,
) -> dict:
    async with session.post(
        url=endpoint, json=pydantic_model.model_dump(mode="json")
    ) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return result
