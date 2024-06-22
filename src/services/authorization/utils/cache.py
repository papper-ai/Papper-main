from src.repositories.redis import RedisRepository


class AuthCache:
    def __init__(self, redis_repository: type(RedisRepository)):
        self.redis: RedisRepository = redis_repository()
        self.cache_prefix = "auth:"

    async def get_login(self, token: str) -> None | str:
        return await self.redis.get(f"{self.cache_prefix}{token}")

    async def set_login(self, token: str, login: str) -> bool:
        return await self.redis.set(f"{self.cache_prefix}{token}", login)


auth_cache_manager = AuthCache(RedisRepository)
