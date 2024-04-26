import aiohttp
from ...schemas.vault import DeleteVaultRequest
from fastapi import HTTPException
from src.utils import aiohttp_error_handler


@aiohttp_error_handler(service_name="Vault")
async def delete_vault_request(
    endpoint: str,
    session: aiohttp.ClientSession,
    pydantic_model: DeleteVaultRequest,
) -> None:
    json_data = pydantic_model.model_dump(mode="json")

    async with session.delete(url=endpoint, json=json_data) as response:
        result = await response.json()
        if response.status >= 400:
            raise HTTPException(status_code=response.status, detail=result["detail"])

    return
