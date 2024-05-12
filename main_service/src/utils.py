import jwt
import asyncio
from fastapi import Request, HTTPException, status
from src.config import settings
import aiohttp
import logging
from functools import wraps


async def decode_jwt(
    token: str,
    public_key: str = settings.jwt_auth.public_key_path.read_text(),
    algorithm: str = settings.jwt_auth.algorithm,
) -> dict:
    try:
        payload = await asyncio.to_thread(
            jwt.decode, jwt=token, key=public_key, algorithms=algorithm
        )
    except jwt.exceptions.ExpiredSignatureError as expired_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except jwt.exceptions.InvalidSignatureError as invalid_signature:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token signature"
        )
    except Exception as generic_error:
        logging.error(generic_error)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token"
        )
    return payload


async def get_aiohttp_session(request: Request) -> aiohttp.ClientSession:
    return request.state.client_session


def aiohttp_error_handler(service_name: str):
    """
    Custom decorator to handle aiohttp errors
    """
    service_name = service_name.capitalize()

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                # Call the decorated function
                return await func(*args, **kwargs)
            except (
                aiohttp.ClientConnectionError | asyncio.TimeoutError
            ) as connect_error:
                logging.error(connect_error)
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"{service_name} service is temporarily unavailable.",
                )
            except aiohttp.ContentTypeError as content_error:
                logging.error(content_error)
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail=f"{service_name} service: invalid content type.",
                )
            except Exception as generic_error:
                logging.error(generic_error)
                if isinstance(generic_error, HTTPException):
                    raise generic_error
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"{service_name} service: an unexpected error occurred.",
                )

        return wrapper

    return decorator
