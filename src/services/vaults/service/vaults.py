import logging
import uuid

from fastapi import UploadFile, HTTPException, status

from ..schemas.vault import (
    VaultPayload,
    CreateVaultRequest,
    VaultCredentials,
    DocumentCredentials,
    UpdateVault,
    VaultPayloadPreview,
)
from ..schemas.document import Document
from src.services.messaging.schemas.chat import ChatCredentials
import asyncio
from ..requests.vault_service import (
    create_vault_request,
    add_document_request,
    delete_vault_request,
    delete_document_request,
    update_vault_name_request,
    get_vault_documents_request,
    get_user_vaults_preview_request,
    get_document_request,
    get_vault_request,
)
from ..schemas.user import UserCredentials
from src.services.messaging.service.messaging import MessagingService
import aiohttp
from ..utils.cache import vaults_cache_manager


class VaultsService:
    def __init__(self) -> None:
        self.cache_manager = vaults_cache_manager

    async def create_vault(
        self,
        create_vault_request_credentials: CreateVaultRequest,
        files: list[UploadFile],
        session: aiohttp.ClientSession,
    ) -> VaultPayload:
        vault_payload = await create_vault_request(
            session=session,
            pydantic_model=create_vault_request_credentials,
            files=files,
        )
        await self.cache_manager.delete_vaults_preview(
            user_id=create_vault_request_credentials.user_id
        )
        await self.cache_manager.set_vault(
            vault_id=vault_payload.id, vault_payload=vault_payload
        )
        return vault_payload

    async def add_document(
        self,
        vault_credentials: VaultCredentials,
        file: UploadFile,
        session: aiohttp.ClientSession,
    ) -> VaultPayload:
        vault_payload = await add_document_request(
            session=session, pydantic_model=vault_credentials, file=file
        )
        await self.cache_manager.set_vault(
            vault_id=vault_payload.id, vault_payload=vault_payload
        )
        return vault_payload

    async def delete_vault_and_chats(
        self,
        user_id: uuid.UUID,
        vault_credentials: VaultCredentials,
        messaging_service: MessagingService,
        session: aiohttp.ClientSession,
    ) -> None:
        chat_payloads = await messaging_service.get_chats_by_vault_id(
            session=session,
            vault_credentials=vault_credentials,
        )

        delete_tasks = []
        for chat_payload in chat_payloads:
            chat_id = chat_payload.id
            chat_credentials = ChatCredentials(chat_id=chat_id)
            delete_tasks.append(
                asyncio.create_task(
                    messaging_service.delete_chat(
                        user_id=user_id,
                        chat_credentials=chat_credentials,
                        session=session,
                    )
                )
            )

        if len(delete_tasks) > 0:
            done, pending = await asyncio.wait(
                delete_tasks, return_when=asyncio.FIRST_EXCEPTION
            )

            for task in pending:
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
        await self.cache_manager.delete_vault(vault_id=vault_credentials.vault_id)
        await self.cache_manager.delete_vaults_preview(user_id=user_id)
        await self.cache_manager.delete_documents(vault_id=vault_credentials.vault_id)
        return

    async def delete_document(
        self, document_credentials: DocumentCredentials, session: aiohttp.ClientSession
    ) -> None:
        await delete_document_request(
            session=session, pydantic_model=document_credentials
        )
        await self.cache_manager.delete_document(
            document_id=document_credentials.document_id
        )
        await self.cache_manager.delete_vault(vault_id=document_credentials.vault_id)
        await self.cache_manager.delete_documents(
            vault_id=document_credentials.vault_id
        )
        return

    async def update_vault_name(
        self,
        user_id: uuid.UUID,
        update_vault_credentials: UpdateVault,
        session: aiohttp.ClientSession,
    ) -> None:
        await update_vault_name_request(
            session=session, pydantic_model=update_vault_credentials
        )
        await self.cache_manager.delete_vault(
            vault_id=update_vault_credentials.vault_id
        )
        await self.cache_manager.delete_vaults_preview(user_id=user_id)
        return

    async def get_vault_documents(
        self, vault_credentials: VaultCredentials, session: aiohttp.ClientSession
    ) -> list[Document]:
        documents = await self.cache_manager.get_documents(
            vault_id=vault_credentials.vault_id
        )
        if documents is None:
            documents = await get_vault_documents_request(
                session=session,
                pydantic_model=vault_credentials,
            )
            await self.cache_manager.set_documents(
                vault_id=vault_credentials.vault_id, documents=documents
            )
        return documents

    async def get_user_vaults_preview(
        self, user_credentials: UserCredentials, session: aiohttp.ClientSession
    ) -> list[VaultPayloadPreview]:
        vaults_preview = await self.cache_manager.get_vaults_preview(
            user_id=user_credentials.user_id
        )
        if vaults_preview is None:
            vaults_preview = await get_user_vaults_preview_request(
                session=session,
                pydantic_model=user_credentials,
            )
            await self.cache_manager.set_vaults_preview(
                user_id=user_credentials.user_id, vaults_preview=vaults_preview
            )
        return vaults_preview

    async def get_vault(
        self, vault_credentials: VaultCredentials, session: aiohttp.ClientSession
    ) -> VaultPayload:
        vault = await self.cache_manager.get_vault(vault_id=vault_credentials.vault_id)
        if vault is None:
            vault = await get_vault_request(
                session=session,
                pydantic_model=vault_credentials,
            )
            await self.cache_manager.set_vault(
                vault_id=vault_credentials.vault_id, vault_payload=vault
            )
        return vault

    async def get_document(
        self, document_credentials: DocumentCredentials, session: aiohttp.ClientSession
    ) -> Document:
        document = await self.cache_manager.get_document(
            document_id=document_credentials.document_id
        )
        if document is None:
            document = await get_document_request(
                session=session,
                pydantic_model=document_credentials,
            )
            await self.cache_manager.set_document(
                document_id=document_credentials.document_id, document=document
            )
        return document
