from redis.asyncio.client import Redis

from conf import RedisConfig


class RedisService:
    def __init__(self, redis_config: RedisConfig):
        config = redis_config.model_dump()
        self.prefix = config.pop("prefix")
        self.__client = Redis(**config)

    async def get_str(self, name: str) -> str | None:
        return await self.__client.get(self.prefix + name)

    async def set_add_with_expires(self, name: str, value: str, time: int = 3600):
        await self.__client.setex(self.prefix + name, time, value)

    async def delete_set(self, name: str):
        await self.__client.delete(self.prefix + name)
