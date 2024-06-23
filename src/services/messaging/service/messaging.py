import uuid

from ..schemas.chat import (
    ChangeChatArchiveStatus,
    CreateChat,
    ChatPayload,
    ChatCredentials,
    UpdateChat,
)
from ..requests.chats_service import (
    get_chat_request,
    get_user_chats_request,
    get_vault_chats_request,
    change_chat_archive_status_request,
    create_chat_request,
    delete_chat_request,
    set_chat_name_request,
)
from ..requests.history_service import (
    get_history_request,
    clean_history_request,
    delete_history_request,
    create_history_request,
)
import aiohttp
import asyncio
import logging
from fastapi import HTTPException, status
from src.services.vaults.schemas.vault import VaultCredentials
from ..schemas.history import HistoryPayload
from ..schemas.user import UserCredentials
from ..requests.external_endpoints import chats_endpoints
from ..utils.cache import messaging_cache_manager


class MessagingService:
    def __init__(self):
        self.cache_manager = messaging_cache_manager

    async def get_chat_by_user_id(
        self,
        session: aiohttp.ClientSession,
        chat_credentials: ChatCredentials,
    ) -> ChatPayload:
        chat_payload = await self.cache_manager.get_chat(
            chat_id=chat_credentials.chat_id
        )

        if chat_payload is None:
            get_chat_request_task = get_chat_request(
                session=session,
                pydantic_model=chat_credentials,
            )
            get_history_request_task = get_history_request(
                session=session, pydantic_model=chat_credentials
            )

            chat_payload, history_payload = await asyncio.gather(
                get_chat_request_task, get_history_request_task
            )

            chat_payload.chat_history = history_payload
            await self.cache_manager.set_chat(
                chat_id=chat_credentials.chat_id, chat_payload=chat_payload
            )

        return chat_payload

    async def get_chats_by_user_id(
        self,
        session: aiohttp.ClientSession,
        user_credentials: UserCredentials,
        is_archived: bool,
    ) -> list[ChatPayload]:
        chat_payloads = await self.cache_manager.get_chats(
            id=user_credentials.user_id, is_archived=is_archived
        )
        if chat_payloads is None:
            endpoint = (
                chats_endpoints.get_user_chats
                if not is_archived
                else chats_endpoints.get_user_archived_chats
            )

            chat_payloads = await get_user_chats_request(
                session=session,
                pydantic_model=user_credentials,
                endpoint=endpoint,
            )

            await self.cache_manager.set_chats(
                id=user_credentials.user_id,
                is_archived=is_archived,
                chat_payloads=chat_payloads,
            )
        return chat_payloads

    async def get_chats_by_vault_id(
        self,
        session: aiohttp.ClientSession,
        vault_credentials: VaultCredentials,
    ) -> list[ChatPayload]:
        # is_archived=False because we don't care about archived status of chats assigned to vault
        chat_payloads = await self.cache_manager.get_chats(
            id=vault_credentials.vault_id, is_archived=False
        )
        if chat_payloads is None:
            chat_payloads = await get_vault_chats_request(
                session=session,
                pydantic_model=vault_credentials,
            )
            await self.cache_manager.set_chats(
                id=vault_credentials.vault_id,
                is_archived=False,
                chat_payloads=chat_payloads,
            )
        return chat_payloads

    async def change_chat_archive_status(
        self,
        user_id: uuid.UUID,
        change_archive_status_credentials: ChangeChatArchiveStatus,
        session: aiohttp.ClientSession,
    ) -> None:
        endpoint = (
            chats_endpoints.archive_chat
            if change_archive_status_credentials.archive_action == "archive"
            else chats_endpoints.unarchive_chat
        )
        await change_chat_archive_status_request(
            session=session,
            pydantic_model=change_archive_status_credentials,
            endpoint=endpoint,
        )
        await self.cache_manager.delete_chat(
            chat_id=change_archive_status_credentials.chat_id
        )
        await self.cache_manager.delete_chats(id=user_id)
        return

    async def clean_chat_history(
        self, chat_credentials: ChatCredentials, session: aiohttp.ClientSession
    ) -> None:
        await clean_history_request(
            session=session,
            pydantic_model=chat_credentials,
        )
        await self.cache_manager.delete_chat(chat_id=chat_credentials.chat_id)
        return

    async def create_chat(
        self, create_chat_credentials: CreateChat, session: aiohttp.ClientSession
    ) -> ChatPayload:
        try:
            chat_payload = await create_chat_request(
                session=session,
                pydantic_model=create_chat_credentials,
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

        await self.cache_manager.set_chat(
            chat_id=chat_payload.id, chat_payload=chat_payload
        )
        await self.cache_manager.delete_chats(id=create_chat_credentials.user_id)
        return chat_payload

    async def delete_chat(
        self,
        user_id: uuid.UUID,
        chat_credentials: ChatCredentials,
        session: aiohttp.ClientSession,
    ) -> None:
        try:
            await delete_history_request(
                session=session, pydantic_model=chat_credentials
            )
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
            await create_history_request(
                session=session, pydantic_model=chat_credentials
            )
            if isinstance(generic_error, HTTPException):
                raise generic_error
            logging.error(generic_error)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Failed to delete chat, for this reason chat history restored",
            )
        await self.cache_manager.delete_chats(id=user_id)
        await self.cache_manager.delete_chat(chat_id=chat_credentials.chat_id)
        return

    async def update_chat_name(
        self,
        user_id: uuid.UUID,
        chat_update_credentials: UpdateChat,
        session: aiohttp.ClientSession,
    ) -> None:
        await set_chat_name_request(
            session=session,
            pydantic_model=chat_update_credentials,
        )
        await self.cache_manager.delete_chat(chat_id=chat_update_credentials.chat_id)
        await self.cache_manager.delete_chats(id=user_id)
        return

    async def get_chat_history(
        self,
        user_id: uuid.UUID,
        chat_credentials: ChatCredentials,
        session: aiohttp.ClientSession,
    ) -> HistoryPayload:
        history = await get_history_request(
            session=session, pydantic_model=chat_credentials
        )
        return history
