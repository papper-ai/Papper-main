from typing import Any

import aiohttp
from src.utils import aiohttp_error_handler
from ...schemas.vault import (
    VaultPayload,
    VaultCredentials,
    DocumentCredentials,
    VaultPayloadPreview,
)
from ...schemas.user import UserCredentials
from ...schemas.document import Document
from fastapi import HTTPException
from ..external_endpoints import vault_endpoints


async def get_info_from_service(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: Any,
) -> list | dict:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.post(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return result


@aiohttp_error_handler(service_name="Vault")
async def get_vault_documents_request(
    session: aiohttp.ClientSession,
    pydantic_model: VaultCredentials,
    endpoint: str = vault_endpoints.get_vault_documents,
) -> list[Document]:
    result = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return [Document(**document) for document in result]


@aiohttp_error_handler(service_name="Vault")
async def get_user_vaults_preview_request(
    session: aiohttp.ClientSession,
    pydantic_model: UserCredentials,
    endpoint: str = vault_endpoints.get_users_vaults,
) -> list[VaultPayloadPreview]:
    result = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return [VaultPayloadPreview(**vault) for vault in result]


@aiohttp_error_handler(service_name="Vault")
async def get_vault_request(
    session: aiohttp.ClientSession,
    pydantic_model: VaultCredentials,
    endpoint: str = vault_endpoints.get_vault_by_id,
) -> VaultPayload:
    result: dict = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )
    return VaultPayload(**result)


@aiohttp_error_handler(service_name="Vault")
async def get_document_request(
    session: aiohttp.ClientSession,
    pydantic_model: DocumentCredentials,
    endpoint: str = vault_endpoints.get_document_by_id,
) -> Document:
    result: dict = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return Document(**result)
