import aiohttp
from fastapi import APIRouter, Depends, Body, Query
from pydantic import UUID4
from ..schemas.chat import CreateChat, ChatPayload
from ..schemas.user import UserCredentials
from ..service import create_chat, get_user_chats
from src.dependencies import parse_jwt, get_aiohttp_session
from src.schemas import JWTPayload
from typing import Annotated

router = APIRouter(prefix="/messaging", tags=["Messaging (Chats & History)"])


@router.post(
    "/create_chat",
    description="Создание чата для беседы с ИИ",
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
    "/get_user_chats",
    response_model=list[ChatPayload],
    description="Получение чатов пользователя (архивированные или нет)",
)
async def getting_user_chats(
    jwt_payload: Annotated[JWTPayload, Depends(parse_jwt)],
    session: Annotated[aiohttp.ClientSession, Depends(get_aiohttp_session)],
    is_archived: Annotated[bool, Query()] = False,
) -> list[ChatPayload]:
    user_credentials = UserCredentials(user_id=jwt_payload.user_id)
    chat_payloads = await get_user_chats(
        session=session, user_credentials=user_credentials, is_archived=is_archived
    )

    return chat_payloads
