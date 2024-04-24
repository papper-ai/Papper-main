import aiohttp
from fastapi import HTTPException, status, UploadFile
import logging
from ..schemas.vault import UpdateVault, VaultResponse, CreateVault
from ..external_endpoints import vault_endpoints


async def create_vault_request(
        endpoint: str,
        session: aiohttp.ClientSession,
        schema: CreateVault,
        files: list[UploadFile],
) -> VaultResponse:
    headers = {"accept": "application/json"}
    json_data = schema.model_dump_json()

    form = aiohttp.FormData()
    form.add_field("create_vault_request", json_data, content_type="application/json")
    for file in files:
        file_bytes = await file.read()
        form.add_field(
            "files", file_bytes, filename=file.filename, content_type=file.content_type
        )

    try:
        async with session.post(url=endpoint, headers=headers, data=form) as response:
            result = await response.json()
            if response.status >= 400:
                raise HTTPException(
                    status_code=response.status, detail=result["detail"]
                )
    except aiohttp.ClientConnectionError as connect_error:
        logging.error(connect_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The vault service is temporarily unable to handle the request.",
        )
    except aiohttp.ContentTypeError as content_error:
        logging.error(content_error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The vault service responded with an invalid content type.",
        )

    return VaultResponse(**result)


async def update_vault_name_request(
        endpoint: str,
        session: aiohttp.ClientSession,
        schema: UpdateVault,
) -> None:
    json_data = schema.model_dump_json()
    try:
        async with session.put(url=endpoint, json=json_data) as response:
            result = await response.json()
            if response.status >= 400:
                raise HTTPException(
                    status_code=response.status, detail=result["detail"]
                )
    except aiohttp.ClientConnectionError as connect_error:
        logging.error(connect_error)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="The vault service is temporarily unable to handle the request.",
        )
    except aiohttp.ContentTypeError as content_error:
        logging.error(content_error)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="The vault service responded with an invalid content type.",
        )
    return
