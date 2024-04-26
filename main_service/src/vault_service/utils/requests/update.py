import aiohttp
from ...schemas.vault import UpdateVaultRequest
from fastapi import HTTPException
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
