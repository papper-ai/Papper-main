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
        async with session.post(
            url=endpoint, json=schema.model_dump_json()
        ) as response:
            result = await response.json()
            if response.status >= 400:
                raise HTTPException(
                    status_code=response.status, detail=result["detail"]
                )
    except aiohttp.ClientConnectionError as connect_error:
        logging.error(connect_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The authorization service is temporarily unable to handle the request.",
        )
    except aiohttp.ContentTypeError as content_error:
        logging.error(content_error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The authorization service responded with an invalid content type.",
        )
    return result
