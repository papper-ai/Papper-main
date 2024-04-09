import aiohttp
from fastapi import HTTPException

from ..schemas import RegistrationCredentials, JWTRefreshRequest, AuthCredentials


async def request_to_auth_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    schema: RegistrationCredentials | JWTRefreshRequest | AuthCredentials,
) -> dict:
    headers = {"accept": "application/json", "Content-Type": "application/json"}

    async with session.post(
        url=endpoint, data=schema.model_dump_json(), headers=headers
    ) as response:
        result = await response.json()
        if response.status != 200:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return result
