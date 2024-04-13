from fastapi import APIRouter, Body, Form, UploadFile, Depends, File
from typing import List
from typing_extensions import Annotated
from ..schemas import VaultCredentials, CreateVault, VaultResponse
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from ..utils import create_vault_request
import aiohttp
from ..external_endpoints import vault_endpoints

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post("/create_vault", response_model=VaultResponse)
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
