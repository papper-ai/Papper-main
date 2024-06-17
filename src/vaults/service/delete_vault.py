import logging
import aiohttp
import asyncio
from ..requests.vault_service import delete_vault_request
from fastapi import HTTPException, status
from src.messaging.requests.chats_service import get_vault_chats_request
from src.messaging.schemas.chat import ChatCredentials
from src.messaging.service import delete_chat
from ..schemas.vault import VaultCredentials


async def delete_vault_and_chats(
    session: aiohttp.ClientSession,
    vault_credentials: VaultCredentials,
) -> None:
    chat_payloads = await get_vault_chats_request(
        session=session,
        pydantic_model=vault_credentials,
    )

    delete_tasks = []
    for chat_payload in chat_payloads:
        chat_id = chat_payload.id
        chat_credentials = ChatCredentials(chat_id=chat_id)
        delete_tasks.append(
            asyncio.create_task(
                delete_chat(chat_credentials=chat_credentials, session=session)
            )
        )

    if len(delete_tasks) > 0:
        done, pending = await asyncio.wait(
            delete_tasks, return_when=asyncio.FIRST_EXCEPTION
        )

        for task in pending:
            #TODO: remove cancelled checking
            if not task.cancelled():
                if task.exception() is None:
                    task.cancel()
        try:
            for task in done:
                if task.exception() is not None:
                    raise task.exception()
        except HTTPException as http_exception:
            logging.error(http_exception)
            raise HTTPException(
                detail="Failed to delete chats, several chats have been not deleted. Vault not deleted too",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        logging.info("No chats to delete")
        await delete_vault_request(session=session, pydantic_model=vault_credentials)
    return
