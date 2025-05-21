from fastapi import FastAPI
from contextlib import asynccontextmanager

from redis.exceptions import ConnectionError as RedisConnectionError

from api.phone_book import router
from config import REDIS_URL
from repositories.contact_repository import ContactRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Управляет подключением к Redis через репозиторий.

    """
    app.state.contact_repository = ContactRepository(REDIS_URL)
    try:
        if await app.state.contact_repository._check_redis_connection():
            print("Успешное подключение к Redis через репозиторий")
        else:
            print("Не удалось подключиться к Redis через репозиторий.")
    except RedisConnectionError as e:
        print(f"Ошибка подключения к Redis: {e}")
    yield
    if hasattr(app.state, 'contact_repository') and app.state.contact_repository:
        await app.state.contact_repository.close()
        print("Соединение с Redis закрыто.")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
