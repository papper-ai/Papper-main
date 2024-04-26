from typing import Any

import aiohttp
from src.utils import aiohttp_error_handler
from ...schemas.vault import (
    GetUserVaultsRequest,
    GetVaultDocumentsRequest,
    VaultCredentials,
    GetVaultRequest,
    GetDocumentRequest,
)
from ...schemas.document import Document
from fastapi import HTTPException


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
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: GetVaultDocumentsRequest,
) -> list:
    result = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return result


@aiohttp_error_handler(service_name="Vault")
async def get_user_vaults_request(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: GetUserVaultsRequest,
) -> list:
    result = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return result


@aiohttp_error_handler(service_name="Vault")
async def get_vault_request(
    endpoint: str, session: aiohttp.ClientSession, pydantic_model: GetVaultRequest
) -> VaultCredentials:
    result: dict = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )
    return VaultCredentials(**result)


@aiohttp_error_handler(service_name="Vault")
async def get_document_request(
    endpoint: str, session: aiohttp.ClientSession, pydantic_model: GetDocumentRequest
) -> Document:
    result: dict = await get_info_from_service(
        endpoint=endpoint, session=session, pydantic_model=pydantic_model
    )

    return Document(**result)
