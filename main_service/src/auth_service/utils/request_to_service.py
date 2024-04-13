import aiohttp
from fastapi import HTTPException, status
import logging

from ..schemas import RegistrationCredentials, JWTRefreshRequest, AuthCredentials


async def request_to_auth_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    schema: RegistrationCredentials | JWTRefreshRequest | AuthCredentials,
) -> dict:
    try:
        async with session.post(url=endpoint, json=schema.model_dump()) as response:
            result = await response.json()
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status, detail=result["detail"]
                )
    except Exception as e:
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Auth service is not available now",
        )
    return result
