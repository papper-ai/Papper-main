from fastapi import APIRouter, Form, UploadFile, Depends, status
from typing import List
from typing_extensions import Annotated
from ..schemas.vault import VaultCredentials, CreateVault, VaultResponse, UpdateVault
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from ..utils.requests_to_service import create_vault_request, update_vault_name_request
import aiohttp
from ..external_endpoints import vault_endpoints

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post(
    "/create_vault",
    response_model=VaultResponse,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового хранилища документов. Тип хранилища `vector` или `graph`",
)
async def create_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    vault_credentials: Annotated[VaultCredentials, Form()],
    files: List[UploadFile],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
):
    create_vault = CreateVault(
        **vault_credentials.model_dump(), user_id=token_payload.user_id
    )

    response: VaultResponse = await create_vault_request(
        endpoint=vault_endpoints.create_vault,
        session=client_session,
        schema=create_vault,
        files=files,
    )
    return response


@router.put(
    "/update_vault_name",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Изменение имени хранилища документов",
)
async def update_vault_name(
    update_vault_credentials: UpdateVault,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> None:
    await update_vault_name_request(
        endpoint=vault_endpoints.update_vault_name,
        session=client_session,
        schema=update_vault_credentials,
    )
