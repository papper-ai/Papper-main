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
from ..service import (
    create_chat,
    get_user_chats,
    get_chat,
    update_chat_name,
    change_chat_archive_status,
    clean_chat_history,
    delete_chat,
)
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from typing import Annotated

router = APIRouter(prefix="/messaging", tags=["Messaging (Chats & History)"])


@router.post(
    "/create_chat",
    description="Создание чата для беседы с ИИ",
    status_code=status.HTTP_201_CREATED,
    response_model=ChatPayload,
)
async def chat_creation(
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    vault_id: Annotated[UUID4, Body()] = "1897e0cd88ee4b86a053972d05212a21",
    name: Annotated[str, Body(max_length=100)] = "Беседа по железобетону",
):
    chat_creation_credentials = CreateChat(
        user_id=jwt_payload.user_id,
        vault_id=vault_id,
        name=name,
    )

    chat_payload = await create_chat(
        registration_credentials=chat_creation_credentials, session=session
    )
    return chat_payload


@router.get(
    "/get_user_chats_preview",
    response_model=list[ChatPayload],
    description="Получение чатов пользователя (архивированные или нет). Если нужны архивированные - то передайте параметр is_archived=true (get_user_chats?is_archived=true). **ЧАТЫ БЕЗ ИСТОРИИ**",
)
async def getting_user_chats(
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    is_archived: Annotated[bool, Query()] = False,
) -> list[ChatPayload]:
    user_credentials = UserCredentials(user_id=jwt_payload.user_id)
    chat_payloads = await get_user_chats(
        session=session,
        user_credentials=user_credentials,
        is_archived=is_archived,
    )
    return chat_payloads


@router.get(
    "/get_chat/{chat_id}",
    response_model=ChatPayload,
    dependencies=[Depends(parse_jwt)],
    description="Получение определённого чата по ID, **ВКЛЮЧАЯ ИСТОРИЮ**",
)
async def getting_particular_chat(
    chat_id: Annotated[UUID4, Path()],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> ChatPayload:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    chat_payload = await get_chat(session=session, chat_credentials=chat_credentials)
    return chat_payload


@router.patch(
    "/rename_chat",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_202_ACCEPTED,
    description="Переименование чата",
)
async def chat_renaming(
    update_chat: UpdateChat,
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> None:
    await update_chat_name(
        session=session,
        chat_update_credentials=update_chat,
    )
    return


@router.patch(
    "/change_chat_archive_status",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Архивирование или разархивирование чата. Ключ __archive_action__ может быть `archive` или `unarchive`",
)
async def chat_archiving(
    archive_chat: ChangeChatArchiveStatus,
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> None:
    await change_chat_archive_status(
        session=session,
        change_archive_status_credentials=archive_chat,
    )
    return


@router.post(
    "/clear_chat_history/{chat_id}",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Очистка истории чата",
)
async def chat_history_cleaning(
    chat_id: Annotated[UUID4, Path()],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> None:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    await clean_chat_history(
        session=session,
        chat_credentials=chat_credentials,
    )
    return


@router.delete(
    "/delete_chat/{chat_id}",
    dependencies=[Depends(parse_jwt)],
    status_code=status.HTTP_204_NO_CONTENT,
    description="Удаление чата и истории",
)
async def chat_deletion(
    chat_id: Annotated[UUID4, Path()],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
) -> None:
    chat_credentials = ChatCredentials(chat_id=chat_id)
    await delete_chat(
        session=session,
        chat_credentials=chat_credentials,
    )
    return
