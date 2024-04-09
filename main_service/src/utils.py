import jwt
import asyncio
from fastapi import Request
import aiohttp
from main_service.src.config import settings


async def decode_jwt(
    token: str,
    public_key: str = settings.jwt_auth.public_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
):
    payload = await asyncio.to_thread(
        jwt.decode(token=token, public_key=public_key, algorithm=algorithm)
    )
    return


async def get_aiohttp_session(request: Request) -> aiohttp.ClientSession:
    return request.state.client_session
