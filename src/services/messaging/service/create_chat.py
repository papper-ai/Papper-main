import logging

import aiohttp
from fastapi import HTTPException, status

from ..schemas.chat import CreateChat, ChatCredentials, ChatPayload
from ..requests.chats_service import create_chat_request, delete_chat_request
from ..requests.history_service import create_history_request


async def create_chat(
    registration_credentials: CreateChat, session: aiohttp.ClientSession
) -> ChatPayload:
    try:
        chat_payload = await create_chat_request(
            session=session,
            pydantic_model=registration_credentials,
        )
    except Exception as generic_error:
        if isinstance(generic_error, HTTPException):
            raise generic_error

        logging.error(generic_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to create chat",
        )

    try:
        await create_history_request(
            session=session,
            pydantic_model=ChatCredentials(chat_id=chat_payload.id),
        )
    except Exception as generic_error:
        await delete_chat_request(
            session=session,
            pydantic_model=ChatCredentials(chat_id=chat_payload.id),
        )

        if isinstance(generic_error, HTTPException):
            raise generic_error
        logging.error(generic_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to create history, for this reason chat was deleted",
        )
    return chat_payload
