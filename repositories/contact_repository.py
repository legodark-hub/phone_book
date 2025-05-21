from fastapi import Request
import redis.asyncio as aioredis
from redis.exceptions import ConnectionError as RedisConnectionError

class ContactRepository:
    def __init__(self, redis_url: str):
        self.redis_client = aioredis.from_url(redis_url)

    async def _check_redis_connection(self):
        """Внутренний метод для проверки соединения с Redis."""
        if not self.redis_client:
            return False
        try:
            await self.redis_client.ping()
            return True
        except RedisConnectionError:
            return False

    async def set_contact(self, phone: str, address: str) -> None:
        """
        Сохраняет или обновляет адрес по указанному номеру телефона в Redis.
        """
        if not await self._check_redis_connection():
            raise ConnectionError("Сервис Redis недоступен в репозитории.")
        await self.redis_client.set(phone, address)

    async def get_contact_address(self, phone: str) -> str | None:
        """
        Получает адрес из Redis по указанному номеру телефона.
        Возвращает None, если номер не найден.
        """
        if not await self._check_redis_connection():
            raise ConnectionError("Сервис Redis недоступен в репозитории.")
        address = await self.redis_client.get(phone)
        if address:
            return address.decode("utf-8")
        return None

    async def close(self):
        """Закрывает соединение с Redis."""
        if self.redis_client:
            await self.redis_client.close()
            
def get_contact_repository(request: Request) -> ContactRepository:
    """
    Возвращает экземпляр ContactRepository, управляемый жизненным циклом приложения.
    Экземпляр хранится в app.state.
    """
    if (
        not hasattr(request.app.state, "contact_repository")
        or request.app.state.contact_repository is None
    ):
        raise RuntimeError(
            "ContactRepository не инициализирован. Проверьте lifespan приложения."
        )
    return request.app.state.contact_repository