from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import Optional

from redis import asyncio as aioredis
from redis.exceptions import ConnectionError as RedisConnectionError

from config import REDIS_URL
from api.phone_book import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Проверяет подключение к Redis.
    """
    redis_client = aioredis.from_url(REDIS_URL)
    try:
        await redis_client.ping()
        print("Успешное подключение к Redis")
    except RedisConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
        redis_client = None
    yield
    if redis_client:
        await redis_client.close()
        print("Соединение с Redis закрыто.")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
