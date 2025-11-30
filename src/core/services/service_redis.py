from functools import wraps

from redis.asyncio.client import Redis

from conf import RedisConfig


def ping(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            await self.__client.ping()
        except Exception as e:
            self.reconnect()  # 尝试重连
        return await func(self, *args, **kwargs)

    return wrapper


class RedisService:
    def __init__(self, redis_config: RedisConfig):
        config = redis_config.model_dump()
        self.prefix = config.pop("prefix")
        self.__client = Redis(**config)
        self.config = config  # 保存redis0配置，用于重连

    async def reconnect(self):
        try:
            await self.__client.aclose()
        except:
            pass
        self.__client = Redis(**self.config)

    @ping
    async def get_str(self, name: str) -> str | None:
        result = await self.__client.get(self.prefix + name)
        if result:
            result = bytes.decode(result)
        return result

    @ping
    async def set_add_with_expires(self, name: str, value: str, time: int = 3600):
        await self.__client.setex(self.prefix + name, time, value)

    @ping
    async def delete_set(self, name: str):
        await self.__client.delete(self.prefix + name)
