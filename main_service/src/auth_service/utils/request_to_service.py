import aiohttp
from fastapi import HTTPException

from ..schemas import RegistrationCredentials, JWTRefreshRequest, AuthCredentials


async def request_to_auth_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    schema: RegistrationCredentials | JWTRefreshRequest | AuthCredentials,
) -> dict:
    async with session.post(url=endpoint, json=schema.model_dump()) as response:
        result = await response.json()
        if response.status != 200:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return result
