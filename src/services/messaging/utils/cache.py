import uuid
from ..schemas.chat import ChatPayload
import json
from src.repositories.redis import RedisRepository


class MessagingCache:
    def __init__(self, redis_repository: type(RedisRepository)):
        self.redis: RedisRepository = redis_repository()
        self.cache_prefix = "messaging:"
        self.chat_prefix = "chat:"
        self.chats_prefix = "chats:"

    async def get_chat(self, chat_id: uuid.UUID) -> None | ChatPayload:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.chat_prefix}{chat_id.hex}"
        )
        chat_payload = ChatPayload.model_validate_json(result) if result else None
        return chat_payload

    async def set_chat(self, chat_id: uuid.UUID, chat_payload: ChatPayload) -> bool:
        str_chat_payload = chat_payload.model_dump_json()
        return await self.redis.set(
            f"{self.cache_prefix}{self.chat_prefix}{chat_id.hex}", str_chat_payload
        )

    async def delete_chat(self, chat_id: uuid.UUID) -> bool:
        return await self.redis.delete(
            f"{self.cache_prefix}{self.chat_prefix}{chat_id.hex}"
        )

    # Use just id not user_id because we also can store payloads by vault_id
    async def get_chats(
        self, id: uuid.UUID, is_archived: bool
    ) -> None | list[ChatPayload]:
        result = await self.redis.get(
            f"{self.cache_prefix}{self.chats_prefix}{id.hex}:{is_archived}"
        )
        json_result = json.loads(result) if result else None
        chat_payloads = (
            [ChatPayload.model_validate_json(chat) for chat in json_result]
            if json_result
            else None
        )
        return chat_payloads

    async def set_chats(
        self, id: uuid.UUID, chat_payloads: list[ChatPayload], is_archived: bool
    ) -> bool:
        str_chat_payloads = [
            chat_payload.model_dump_json() for chat_payload in chat_payloads
        ]
        json_chat_payloads = json.dumps(str_chat_payloads)
        return await self.redis.set(
            f"{self.cache_prefix}{self.chats_prefix}{id.hex}:{is_archived}",
            json_chat_payloads,
        )

    async def delete_chats(self, id: uuid.UUID) -> None:
        await self.redis.delete_by_pattern(
            pattern=f"{self.cache_prefix}{self.chats_prefix}{id.hex}:*"
        )
        return


messaging_cache_manager = MessagingCache(RedisRepository)
