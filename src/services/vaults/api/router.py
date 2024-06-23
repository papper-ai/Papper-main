from fastapi import APIRouter, Form, UploadFile, Depends, status
from typing import List, Annotated
from ..schemas.vault import (
    VaultPayload,
    VaultPayloadPreview,
    CreateVault,
    CreateVaultRequest,
    UpdateVault,
    VaultCredentials,
    DocumentCredentials,
)
from ..schemas.user import UserCredentials
from ..schemas.document import Document
from src.dependencies import parse_jwt_bearer, get_aiohttp_session
from src.schemas import JWTPayload
from src.services.messaging.service.messaging import MessagingService
from src.services.messaging.api.dependencies import get_messaging_service
from .dependencies import get_vaults_service
from ..service.vaults import VaultsService
import aiohttp
from pydantic import UUID4

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post(
    "",
    response_model=VaultPayload,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового хранилища документов. Тип хранилища `vector` или `graph`",
)
async def create_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    create_vault_credentials: Annotated[CreateVault, Form()],
    files: List[UploadFile],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> VaultPayload:
    create_vault_request_credentials = CreateVaultRequest(
        **create_vault_credentials.model_dump(), user_id=token_payload.user_id
    )

    response = await vaults_service.create_vault(
        session=client_session,
        create_vault_request_credentials=create_vault_request_credentials,
        files=files,
    )
    return response


@router.patch(
    "/document",
    dependencies=[Depends(parse_jwt_bearer)],
    status_code=status.HTTP_201_CREATED,
    response_model=VaultPayload,
    description="Загрузка нового документа в существующее хранилище",
)
async def upload_document(
    vault_id: Annotated[UUID4, Form()],
    file: UploadFile,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> VaultPayload:
    results = await vaults_service.add_document(
        session=client_session,
        vault_credentials=VaultCredentials(vault_id=vault_id),
        file=file,
    )
    return results


@router.delete(
    "/{vault_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление хранилища документов",
)
async def delete_vault(
    vault_id: UUID4,
    token_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> None:
    await vaults_service.delete_vault_and_chats(
        user_id=token_payload.user_id,
        vault_credentials=VaultCredentials(vault_id=vault_id),
        messaging_service=messaging_service,
        session=client_session,
    )
    return


@router.delete(
    "/{vault_id}/document/{document_id}",
    dependencies=[Depends(parse_jwt_bearer)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление документа из хранилища",
)
async def delete_document(
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vault_id: UUID4,
    document_id: UUID4,
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> None:
    await vaults_service.delete_document(
        session=client_session,
        document_credentials=DocumentCredentials(
            vault_id=vault_id, document_id=document_id
        ),
    )
    return


@router.patch(
    "/name",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Изменение имени хранилища документов",
)
async def update_vault_name(
    update_vault_credentials: UpdateVault,
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> None:
    await vaults_service.update_vault_name(
        user_id=jwt_payload.user_id,
        session=client_session,
        update_vault_credentials=update_vault_credentials,
    )
    return


@router.get(
    "/{vault_id}/documents",
    dependencies=[Depends(parse_jwt_bearer)],
    response_model=list[Document],
    description="Получение всех документов, находящихся в хранилище.",
)
async def get_vault_documents(
    vault_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> list[Document]:
    response = await vaults_service.get_vault_documents(
        session=client_session,
        vault_credentials=VaultCredentials(vault_id=vault_id),
    )
    return response


@router.get(
    "/vaults/preview",
    response_model=list[VaultPayloadPreview],
    description="Получение превью списка хранилищ, созданных пользователем. **Данные извлекаются из токена!**",
)
async def get_users_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> list:
    response = await vaults_service.get_user_vaults_preview(
        session=client_session,
        user_credentials=UserCredentials(user_id=token_payload.user_id),
    )
    return response


@router.get(
    "/{vault_id}",
    dependencies=[Depends(parse_jwt_bearer)],
    response_model=VaultPayload,
    description="Получение **ВСЕХ** данных о хранилище.",
)
async def get_vault(
    vault_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> VaultPayload:
    response = await vaults_service.get_vault(
        session=client_session,
        vault_credentials=VaultCredentials(vault_id=vault_id),
    )
    return response


@router.get(
    "/document/{document_id}",
    dependencies=[Depends(parse_jwt_bearer)],
    response_model=Document,
    description="Получение **ВСЕХ** о определенном документе из хранилища.",
)
async def get_document(
    document_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vaults_service: Annotated[VaultsService, Depends(get_vaults_service)],
) -> Document:
    response = await vaults_service.get_document(
        session=client_session,
        document_credentials=DocumentCredentials(document_id=document_id),
    )
    return response
