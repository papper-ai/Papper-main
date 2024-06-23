import aiohttp
from fastapi import APIRouter, Depends, Body, Query, status, Path
from pydantic import UUID4
from ..schemas.chat import (
    CreateChat,
    ChatPayload,
    ChatCredentials,
    UpdateChat,
    ChangeChatArchiveStatus,
)
from ..schemas.user import UserCredentials
from .dependencies import get_messaging_service
from ..service.messaging import MessagingService
from src.dependencies import parse_jwt_bearer, get_aiohttp_session
from src.schemas import JWTPayload
from typing import Annotated

router = APIRouter(prefix="/messaging", tags=["Messaging (Chats & History)"])


@router.post(
    "/chat",
    description="Создание чата для беседы с ИИ",
    status_code=status.HTTP_201_CREATED,
    response_model=ChatPayload,
)
async def chat_creation(
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
    vault_id: Annotated[UUID4, Body()] = "1897e0cd88ee4b86a053972d05212a21",
    name: Annotated[str, Body(max_length=100)] = "Беседа по железобетону",
):
    chat_creation_credentials = CreateChat(
        user_id=jwt_payload.user_id,
        vault_id=vault_id,
        name=name,
    )

    chat_payload = await messaging_service.create_chat(
        create_chat_credentials=chat_creation_credentials, session=session
    )
    return chat_payload


@router.get(
    "/chats/preview",
    response_model=list[ChatPayload],
    description="Получение чатов пользователя (архивированные или нет). Если нужны архивированные - то передайте параметр is_archived=true (get_user_chats?is_archived=true). **ЧАТЫ БЕЗ ИСТОРИИ**",
)
async def getting_user_chats(
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
    is_archived: Annotated[bool, Query()] = False,
) -> list[ChatPayload]:
    user_credentials = UserCredentials(user_id=jwt_payload.user_id)
    chat_payloads = await messaging_service.get_chats_by_user_id(
        session=session, user_credentials=user_credentials, is_archived=is_archived
    )
    return chat_payloads


@router.get(
    "/chat/{chat_id}",
    response_model=ChatPayload,
    dependencies=[Depends(parse_jwt_bearer)],
    description="Получение определённого чата по ID, **ВКЛЮЧАЯ ИСТОРИЮ**",
)
async def getting_particular_chat(
    chat_id: Annotated[UUID4, Path()],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> ChatPayload:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    chat_payload = await messaging_service.get_chat_by_user_id(
        session=session, chat_credentials=chat_credentials
    )
    return chat_payload


@router.patch(
    "/chat/renaming",
    status_code=status.HTTP_202_ACCEPTED,
    description="Переименование чата",
)
async def chat_renaming(
    update_chat: UpdateChat,
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> None:
    await messaging_service.update_chat_name(
        user_id=jwt_payload.user_id,
        session=session,
        chat_update_credentials=update_chat,
    )
    return


@router.patch(
    "/chat/archive-status",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Архивирование или разархивирование чата. Ключ __archive_action__ может быть `archive` или `unarchive`",
)
async def chat_archiving(
    archive_chat: ChangeChatArchiveStatus,
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> None:
    await messaging_service.change_chat_archive_status(
        user_id=jwt_payload.user_id,
        session=session,
        change_archive_status_credentials=archive_chat,
    )
    return


@router.post(
    "/chat/{chat_id}/history/cleaning",
    dependencies=[Depends(parse_jwt_bearer)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Очистка истории чата",
)
async def chat_history_cleaning(
    chat_id: Annotated[UUID4, Path()],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> None:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    await messaging_service.clean_chat_history(
        session=session,
        chat_credentials=chat_credentials,
    )
    return


@router.delete(
    "/chat/{chat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление чата и истории",
)
async def chat_deletion(
    chat_id: Annotated[UUID4, Path()],
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt_bearer)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    messaging_service: Annotated[MessagingService, Depends(get_messaging_service)],
) -> None:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    await messaging_service.delete_chat(
        user_id=jwt_payload.user_id,
        session=session,
        chat_credentials=chat_credentials,
    )
    return
