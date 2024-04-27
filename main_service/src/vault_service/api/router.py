from fastapi import APIRouter, Form, UploadFile, Depends, status, Body, Path
from typing import List
from typing_extensions import Annotated
from ..schemas.vault import (
    VaultCredentials,
    AddDocumentRequest,
    PreviewVaultCredentials,
    CreateVault,
    CreateVaultRequest,
    CreateVaultResponse,
    UpdateVaultRequest,
    DeleteVaultRequest,
    DeleteDocumentRequest,
    UpdateVault,
    GetVaultDocumentsRequest,
    GetUserVaultsRequest,
    GetVaultRequest,
    GetDocumentRequest,
)
from ..schemas.document import Document
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from ..utils.requests import (
    create_vault_request,
    add_document_request,
    update_vault_name_request,
    delete_vault_request,
    delete_document_request,
    get_vault_documents_request,
    get_user_vaults_request,
    get_vault_request,
    get_document_request,
)
import aiohttp
from ..external_endpoints import vault_endpoints
from pydantic import UUID4

router = APIRouter(prefix="/vault", tags=["Documents & Vaults"])


@router.post(
    "/create_vault",
    response_model=CreateVaultResponse,
    status_code=status.HTTP_201_CREATED,
    description="Создание нового хранилища документов. Тип хранилища `vector` или `graph`",
)
async def create_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    create_vault_credentials: Annotated[CreateVault, Form()],
    files: List[UploadFile],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> CreateVaultResponse:
    create_vault_request_credentials = CreateVaultRequest(
        **create_vault_credentials.model_dump(), user_id=token_payload.user_id
    )

    response = await create_vault_request(
        endpoint=vault_endpoints.create_vault,
        session=client_session,
        pydantic_model=create_vault_request_credentials,
        files=files,
    )
    return response


@router.post(
    "/upload_document",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_201_CREATED,
    response_model=VaultCredentials,
    description="Загрузка нового документа в существующее хранилище",
)
async def upload_document(
    vault_id: Annotated[UUID4, Form()],
    file: UploadFile,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> VaultCredentials:

    results = await add_document_request(
        endpoint=vault_endpoints.add_document,
        session=client_session,
        pydantic_model=AddDocumentRequest(vault_id=vault_id),
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
        endpoint=vault_endpoints.delete_vault,
        session=client_session,
        pydantic_model=DeleteVaultRequest(vault_id=vault_id),
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
        endpoint=vault_endpoints.delete_document,
        session=client_session,
        pydantic_model=DeleteDocumentRequest(
            vault_id=vault_id, document_id=document_id
        ),
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
    update_vault = UpdateVaultRequest(
        name=update_vault_credentials.new_name,
        vault_id=update_vault_credentials.vault_id,
    )

    await update_vault_name_request(
        endpoint=vault_endpoints.rename_vault,
        session=client_session,
        pydantic_model=update_vault,
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
        endpoint=vault_endpoints.get_vault_documents,
        session=client_session,
        pydantic_model=GetVaultDocumentsRequest(vault_id=vault_id),
    )

    return response


@router.get(
    "/get_user_vaults",
    response_model=list[PreviewVaultCredentials],
    description="Получение списка хранилищ, созданных пользователем. **Данные извлекаются из токена!**",
)
async def get_users_vaults(
    token_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> list:

    response = await get_user_vaults_request(
        endpoint=vault_endpoints.get_users_vaults,
        session=client_session,
        pydantic_model=GetUserVaultsRequest(user_id=token_payload.user_id),
    )

    return response


@router.get(
    "/get_vault/{vault_id}",
    dependencies=[Depends(parse_jwt)],
    response_model=VaultCredentials,
    description="Получение метаданных хранилища.",
)
async def get_vault(
    vault_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> VaultCredentials:
    response = await get_vault_request(
        endpoint=vault_endpoints.get_vault_by_id,
        session=client_session,
        pydantic_model=GetVaultRequest(vault_id=vault_id),
    )
    return response


@router.get(
    "/get_document/{document_id}",
    dependencies=[Depends(parse_jwt)],
    response_model=Document,
    description="Получение метаданных документа из хранилища.",
)
async def get_document(
    document_id: UUID4,
    client_session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> Document:
    response = await get_document_request(
        endpoint=vault_endpoints.get_document_by_id,
        session=client_session,
        pydantic_model=GetDocumentRequest(document_id=document_id),
    )
    return response
