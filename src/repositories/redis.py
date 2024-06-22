from contextlib import asynccontextmanager
from typing import AsyncIterator
import redis.asyncio as aioredis
from .abstract import KeyValueDBAbstractRepository
from src.config import settings
import logging


class RedisRepository(KeyValueDBAbstractRepository):
    client: aioredis.Redis = aioredis.Redis(
        host=settings.redis_host, port=settings.redis_port, decode_responses=True
    )
    client_cache_ttl = settings.client_cache_ttl

    @asynccontextmanager
    async def redis_transaction(self) -> AsyncIterator[aioredis.client.Pipeline]:
        pipe = self.client.pipeline(transaction=True)
        try:
            yield pipe
            await pipe.execute()
        except Exception as generic_error:
            await pipe.discard()
            logging.error(f"Redis transaction error: {generic_error}")
        finally:
            await pipe.close()

    async def set(self, key, value, ttl: int | None = None) -> bool:
        ttl = self.client_cache_ttl if ttl is None else ttl
        return await self.client.set(key, value, ex=ttl)

    async def delete(self, key) -> bool:
        return await self.client.delete(key)

    async def get(self, key):
        value = await self.client.get(key)
        return value

    async def clear(self):
        return await self.client.flushdb()
