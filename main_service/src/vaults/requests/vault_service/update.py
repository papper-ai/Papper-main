import aiohttp
from ...schemas.vault import (
    VaultPayload,
    VaultCredentials,
    UpdateVault,
)
from fastapi import HTTPException, UploadFile
from src.utils import aiohttp_error_handler
from ..external_endpoints import vault_endpoints


@aiohttp_error_handler(service_name="Vault")
async def update_vault_name_request(
    session: aiohttp.ClientSession,
    pydantic_model: UpdateVault,
    endpoint: str = vault_endpoints.rename_vault,
) -> None:
    json_data = pydantic_model.model_dump(mode="json", by_alias=True)

    async with session.patch(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return


@aiohttp_error_handler(service_name="Vault")
async def add_document_request(
    session: aiohttp.ClientSession,
    pydantic_model: VaultCredentials,
    file: UploadFile,
    endpoint: str = vault_endpoints.add_document,
) -> VaultPayload:
    headers = {"accept": "application/json"}
    json_data = pydantic_model.vault_id.hex

    form = aiohttp.FormData(quote_fields=False)
    form.add_field("vault_id", json_data, content_type="application/json")
    file_bytes = await file.read()
    form.add_field(
        "file", file_bytes, filename=file.filename, content_type=file.content_type
    )

    timeout = aiohttp.ClientTimeout(total=60 * 3)
    async with session.post(
        url=endpoint, headers=headers, data=form, timeout=timeout
    ) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])
    return VaultPayload(**result)
