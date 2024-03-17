from aiohttp_session import session_middleware
from aiohttp_session.redis_storage import RedisStorage
from redis.asyncio import Redis


session_storage_middleware = session_middleware(
    RedisStorage(
        Redis(host='localhost', port=6379),
    ),
)
