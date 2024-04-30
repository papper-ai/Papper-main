from fastapi import APIRouter, Form, UploadFile, Depends, status, Body, Path
from typing import List
from typing_extensions import Annotated
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
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from ..requests.vault_service import (
    create_vault_request,
    add_document_request,
    update_vault_name_request,
    delete_vault_request,
    delete_document_request,
    get_vault_documents_request,
    get_user_vaults_preview_request,
    get_vault_request,
    get_document_request,
)
import aiohttp
from pydantic import UUID4

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post(
    "/create_vault",
    response_model=VaultPayload,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового хранилища документов. Тип хранилища `vector` или `graph`",
)
async def create_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    create_vault_credentials: Annotated[CreateVault, Form()],
    files: List[UploadFile],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> VaultPayload:
    create_vault_request_credentials = CreateVaultRequest(
        **create_vault_credentials.model_dump(), user_id=token_payload.user_id
    )

    response = await create_vault_request(
        session=client_session,
        pydantic_model=create_vault_request_credentials,
        files=files,
    )
    return response


@router.post(
    "/upload_document",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_201_CREATED,
    response_model=VaultPayload,
    description="Загрузка нового документа в существующее хранилище",
)
async def upload_document(
    vault_id: Annotated[UUID4, Form()],
    file: UploadFile,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> VaultPayload:

    results = await add_document_request(
        session=client_session,
        pydantic_model=VaultCredentials(vault_id=vault_id),
        file=file,
    )
    return results


@router.delete(
    "/delete_vault/{vault_id}",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление хранилища документов",
)
async def delete_vault(
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vault_id: UUID4,
) -> None:
    await delete_vault_request(
        session=client_session,
        pydantic_model=VaultCredentials(vault_id=vault_id),
    )
    return


@router.delete(
    "/delete_document/{vault_id}/{document_id}",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление документа из хранилища",
)
async def delete_document(
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vault_id: UUID4,
    document_id: UUID4,
) -> None:

    await delete_document_request(
        session=client_session,
        pydantic_model=DocumentCredentials(vault_id=vault_id, document_id=document_id),
    )

    return


@router.patch(
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
        session=client_session,
        pydantic_model=update_vault_credentials,
    )

    return


@router.get(
    "/get_vault_documents/{vault_id}",
    dependencies=[Depends(parse_jwt)],
    response_model=list[Document],
    description="Получение всех документов, находящихся в хранилище.",
)
async def get_vault_documents(
    vault_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> list:
    response = await get_vault_documents_request(
        session=client_session,
        pydantic_model=VaultCredentials(vault_id=vault_id),
    )
    return response


@router.get(
    "/get_user_vaults_preview",
    response_model=list[VaultPayloadPreview],
    description="Получение превью списка хранилищ, созданных пользователем. **Данные извлекаются из токена!**",
)
async def get_users_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> list:
    response = await get_user_vaults_preview_request(
        session=client_session,
        pydantic_model=UserCredentials(user_id=token_payload.user_id),
    )
    return response


@router.get(
    "/get_vault/{vault_id}",
    dependencies=[Depends(parse_jwt)],
    response_model=VaultPayload,
    description="Получение **ВСЕХ** данных о хранилище.",
)
async def get_vault(
    vault_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> VaultPayload:
    response = await get_vault_request(
        session=client_session,
        pydantic_model=VaultCredentials(vault_id=vault_id),
    )
    return response


@router.get(
    "/get_document/{document_id}",
    dependencies=[Depends(parse_jwt)],
    response_model=Document,
    description="Получение **ВСЕХ** о определенном документе из хранилища.",
)
async def get_document(
    document_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> Document:
    response = await get_document_request(
        session=client_session,
        pydantic_model=DocumentCredentials(document_id=document_id),
    )
    return response
