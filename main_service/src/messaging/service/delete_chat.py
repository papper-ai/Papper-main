import aiohttp
from fastapi import HTTPException, status
import logging

from ..schemas.chat import ChatCredentials
from ..requests.history_service import delete_history_request, create_history_request
from ..requests.chats_service import delete_chat_request


async def delete_chat(
    chat_credentials: ChatCredentials, session: aiohttp.ClientSession
) -> None:
    try:
        await delete_history_request(session=session, pydantic_model=chat_credentials)
    except Exception as generic_error:
        if isinstance(generic_error, HTTPException):
            raise generic_error

        logging.error(generic_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to delete chat history",
        )

    try:
        await delete_chat_request(session=session, pydantic_model=chat_credentials)
    except Exception as generic_error:
        await create_history_request(session=session, pydantic_model=chat_credentials)
        if isinstance(generic_error, HTTPException):
            raise generic_error
        logging.error(generic_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to delete chat, for this reason chat history restored",
        )
    return
