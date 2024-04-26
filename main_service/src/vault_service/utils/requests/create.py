import aiohttp
from ...schemas.vault import CreateVaultRequest, CreateVaultResponse
from ...schemas.document import Document
from fastapi import UploadFile, HTTPException
from src.utils import aiohttp_error_handler


@aiohttp_error_handler(service_name="Vault")
async def create_vault_request(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: CreateVaultRequest,
    files: list[UploadFile],
) -> CreateVaultResponse:
    headers = {"accept": "application/json"}
    json_data = pydantic_model.model_dump_json()

    form = aiohttp.FormData()
    form.add_field("create_vault_request", json_data, content_type="application/json")
    for file in files:
        file_bytes = await file.read()
        form.add_field(
            "files", file_bytes, filename=file.filename, content_type=file.content_type
        )

    async with session.post(url=endpoint, headers=headers, data=form) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return CreateVaultResponse(**result)
