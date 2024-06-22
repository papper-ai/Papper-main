import redis.asyncio as aioredis
from .abstract import KeyValueDBAbstractRepository
from src.config import settings


class RedisRepository(KeyValueDBAbstractRepository):
    client: aioredis.Redis = aioredis.Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )

    async def set(self, key, value) -> bool:
        await self.client.set(key, value)
        return True

    async def delete(self, key) -> bool:
        await self.client.delete(key)
        return True

    async def get(self, key):
        value = await self.client.get(key)
        return value

    async def clear(self):
        await self.client.flushdb()
