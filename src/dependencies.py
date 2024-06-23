from fastapi import Request, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import aiohttp
from typing_extensions import Annotated
from src.utils import decode_jwt
from src.schemas import JWTPayload

http_bearer = HTTPBearer()


async def get_aiohttp_session(request: Request) -> aiohttp.ClientSession:
    return request.state.client_session


async def parse_jwt_bearer(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(http_bearer)],
) -> JWTPayload:
    token = credentials.credentials
    dict_payload = await decode_jwt(token=token)
    payload = JWTPayload.model_validate(dict_payload)
    return payload


async def parse_jwt_token(token: str | None = None) -> JWTPayload:
    dict_payload = await decode_jwt(token=token)
    payload = JWTPayload.model_validate(dict_payload)
    return payload
