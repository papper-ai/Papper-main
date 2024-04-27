import aiohttp
from ...schemas.vault import UpdateVaultRequest, AddDocumentRequest, VaultCredentials
from fastapi import HTTPException, UploadFile
from src.utils import aiohttp_error_handler


@aiohttp_error_handler(service_name="Vault")
async def update_vault_name_request(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: UpdateVaultRequest,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.patch(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return


@aiohttp_error_handler(service_name="Vault")
async def add_document_request(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: AddDocumentRequest,
    file: UploadFile,
) -> VaultCredentials:
    headers = {"accept": "application/json"}
    json_data = pydantic_model.vault_id.hex

    form = aiohttp.FormData()
    form.add_field("vault_id", json_data, content_type="application/json")
    file_bytes = await file.read()
    form.add_field(
        "file", file_bytes, filename=file.filename, content_type=file.content_type
    )

    async with session.post(url=endpoint, headers=headers, data=form) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return VaultCredentials(**result)
