import aiohttp
from ...schemas.vault import VaultCredentials, DocumentCredentials
from fastapi import HTTPException
from src.utils import aiohttp_error_handler
from ..external_endpoints import vault_endpoints


@aiohttp_error_handler(service_name="Vault")
async def delete_vault_request(
    session: aiohttp.ClientSession,
    pydantic_model: VaultCredentials,
    endpoint: str = vault_endpoints.delete_vault,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.delete(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return


@aiohttp_error_handler(service_name="Vault")
async def delete_document_request(
    session: aiohttp.ClientSession,
    pydantic_model: DocumentCredentials,
    endpoint: str = vault_endpoints.delete_document,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.delete(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return
